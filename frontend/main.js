const submitBtn = document.getElementById('submitBtn');
const clearBtn = document.getElementById('clearBtn');
const inputText = document.getElementById('inputText');
const output = document.getElementById('output');

function showStatus(type, text) {
  output.style.display = 'block';
  output.innerHTML = `<div class="status ${type}">${getStatusIcon(type)}${text}</div>`;
}
function showJsonBlock(obj) {
  output.innerHTML += `<div class="json-block">${syntaxHighlight(JSON.stringify(obj, null, 2))}</div>`;
}
function getStatusIcon(type) {
  switch(type) {
    case 'success': return '✅ ';
    case 'error': return '❌ ';
    case 'info': return 'ℹ️ ';
    case 'warning': return '⚠️ ';
    case 'loading': return '<span class="loader"></span>';
    default: return '';
  }
}
function syntaxHighlight(json) {
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(\.\d*)?([eE][+\-]?\d+)?)/g, function (match) {
    let cls = 'number';
    if (/^"/.test(match)) {
      if (/:$/.test(match)) cls = 'key';
      else cls = 'string';
    } else if (/true|false/.test(match)) cls = 'boolean';
    else if (/null/.test(match)) cls = 'null';
    return `<span class="${cls}">${match}</span>`;
  });
}

clearBtn.onclick = () => {
  inputText.value = '';
  output.style.display = 'none';
};

submitBtn.onclick = async () => {
  output.style.display = 'block';
  showStatus('loading', 'Sending message to classifier agent...');
  submitBtn.disabled = true;
  clearBtn.disabled = true;
  const message = inputText.value.trim();
  if (!message) {
    showStatus('warning', 'Please enter a message.');
    submitBtn.disabled = false;
    clearBtn.disabled = false;
    return;
  }

  // Step 1: Classify
  let classify;
  try {
    classify = await fetch('http://localhost:5004/classify', {
      method: 'POST',
      headers: {'Content-Type': 'text/plain'},
      body: message
    }).then(r => r.json());
    showStatus('success', 'Classifier Response:');
    showJsonBlock(classify);
  } catch (e) {
    showStatus('error', 'Failed to contact classifier: ' + e);
    submitBtn.disabled = false;
    clearBtn.disabled = false;
    return;
  }

  const format = (classify.format || '').toLowerCase();
  const intent = (classify.intent || '').toLowerCase();

  showStatus('info', `Redirecting you to <b>${format}</b> agent...`);
  showJsonBlock(classify);

  // Step 2: Route based on intent
  try {
    if (intent === "order placement") {
      showStatus('info', '📦 Order intent detected... Submitting order...');
      let name = "Unknown", email = "Unknown";
      try {
        const parsed = JSON.parse(message);
        name = parsed.name || "Unknown";
        email = parsed.email || "Unknown";
      } catch {}
      const items = await fetch('http://localhost:5004/extract_items', {
        method: 'POST',
        headers: {'Content-Type': 'text/plain'},
        body: message
      }).then(r => r.json()).catch(() => ({}));
      const products = Object.entries(items).map(([name, quantity]) => ({name, quantity}));
      const order_id = Math.random().toString(36).slice(2,10);
      const payload = {type: "Order Placement", order_id, name, email, products};
      const memRes = await fetch('http://localhost:5003/memory', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      }).then(r => r.json());
      showStatus('success', '🧠 Memory Agent Response:');
      showJsonBlock(memRes);
    } else if (intent === "rfq") {
      showStatus('info', '📨 RFQ intent detected... Checking stock...');
      const rfqRes = await fetch('http://localhost:5005/json/RFQ', {
        method: 'GET',
        headers: {'Content-Type': 'text/plain'},
        body: message
      }).then(r => r.json());
      showStatus('success', '📄 RFQ Agent Response:');
      showJsonBlock(rfqRes);
    } else if (intent === "complaint") {
      showStatus('info', '⚠️ Complaint intent detected... Submitting complaint...');
      const complaintRes = await fetch('http://localhost:5003/memory', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: "complaint", message})
      }).then(r => r.json());
      showStatus('success', '🧠 Memory Agent Response:');
      showJsonBlock(complaintRes);
    } else if (intent === "invoice") {
      showStatus('info', '🧾 Invoice intent detected... Fetching invoice...');
      const order_id = (message.match(/[a-z0-9]{8}/i) || [])[0] || "unknown";
      const invoiceRes = await fetch(`http://localhost:5000/get/${order_id}`).then(r => r.json());
      showStatus('success', '📑 Invoice Agent Response:');
      showJsonBlock(invoiceRes);
    } else {
      showStatus('warning', `No special routing for this intent (${intent}).`);
    }
  } catch (e) {
    showStatus('error', 'Error: ' + e);
  }
  submitBtn.disabled = false;
  clearBtn.disabled = false;
};