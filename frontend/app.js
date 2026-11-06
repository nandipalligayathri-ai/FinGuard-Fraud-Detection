const API = "http://127.0.0.1:8000";
const token = localStorage.getItem("token");
if (!token) location.href = "login.html";
const headers = {"Authorization": `Bearer ${token}`};

async function api(path, options={}) {
  const response = await fetch(`${API}${path}`, {...options, headers:{...headers,...(options.headers||{})}});
  if (response.status === 401) { localStorage.removeItem("token"); location.href="login.html"; }
  if (!response.ok) { const error=await response.json().catch(()=>({detail:"Request failed"})); throw new Error(error.detail||"Request failed"); }
  return response.json();
}
async function loadDashboard() {
  try {
    const s = await api("/api/dashboard/summary");
    document.getElementById("totalTransactions").textContent = s.total_transactions;
    document.getElementById("totalAlerts").textContent = s.total_alerts;
    document.getElementById("pendingAlerts").textContent = s.pending_alerts;
    document.getElementById("totalAmount").textContent = new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:0}).format(s.total_amount);
    await loadAlerts();
  } catch(e) { document.getElementById("message").textContent = e.message; }
}
async function loadAlerts() {
  const status = document.getElementById("statusFilter").value;
  const items = await api(`/api/alerts/${status ? "?status="+encodeURIComponent(status) : ""}`);
  const body = document.getElementById("alertsBody");
  if (!items.length) { body.innerHTML='<tr><td colspan="7">No alerts found.</td></tr>'; return; }
  body.innerHTML = items.map(a => `<tr>
    <td>${a.alert_id}</td><td>${a.transaction_id}</td><td class="score">${a.risk_score}/100</td>
    <td>${escapeHtml(a.rule_name)}</td><td>${escapeHtml(a.reason)}</td><td><span class="status">${a.review_status}</span></td>
    <td><select class="action-select" data-id="${a.alert_id}"><option value="">Change status</option><option>PENDING</option><option>UNDER_REVIEW</option><option>CLEARED</option><option>CLOSED</option></select></td>
  </tr>`).join("");
  body.querySelectorAll("select[data-id]").forEach(el => el.addEventListener("change", async e => {
    if (!e.target.value) return;
    try { await api(`/api/alerts/${e.target.dataset.id}`,{method:"PATCH",headers:{"Content-Type":"application/json"},body:JSON.stringify({review_status:e.target.value})}); await loadDashboard(); }
    catch(err) { alert(err.message); }
  }));
}
function escapeHtml(value) { return String(value ?? "").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
document.getElementById("refreshBtn").addEventListener("click", loadDashboard);
document.getElementById("statusFilter").addEventListener("change", loadAlerts);
document.getElementById("logoutBtn").addEventListener("click",()=>{localStorage.removeItem("token");location.href="login.html";});
document.getElementById("importBtn").addEventListener("click", async()=>{
  const file=document.getElementById("csvFile").files[0]; const message=document.getElementById("message");
  if(!file){message.textContent="Choose a CSV file first.";return;}
  const form=new FormData();form.append("file",file);
  try {const result=await api("/api/transactions/import",{method:"POST",body:form});message.textContent=`Imported ${result.created} transactions. Errors: ${result.errors.length}.`;await loadDashboard();}
  catch(e){message.textContent=e.message;}
});
loadDashboard();
