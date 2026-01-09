let timeGranularity = "Daily";
let dataView = "Orders";

let chartInstance;
let rawData = [];
let workbook;

/* ===============================
   Excel Date → JS Date
================================ */
function excelDateToJSDate(serial) {
  const utc_days = Math.floor(serial - 25569);
  return new Date(utc_days * 86400 * 1000);
}

/* ===============================
   Time Key Generator
================================ */
function getTimeKey(excelDate) {
  const d = typeof excelDate === "number"
    ? excelDateToJSDate(excelDate)
    : new Date(excelDate);

  if (timeGranularity === "Daily") {
    return d.toISOString().slice(0, 10);
  }

  if (timeGranularity === "Monthly") {
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  }

  if (timeGranularity === "Weekly") {
    const temp = new Date(d);
    temp.setDate(temp.getDate() + 3 - (temp.getDay() + 6) % 7);
    const week1 = new Date(temp.getFullYear(), 0, 4);
    const week = 1 + Math.round(
      ((temp - week1) / 86400000 - 3 + (week1.getDay() + 6) % 7) / 7
    );
    return `${temp.getFullYear()}-W${String(week).padStart(2, "0")}`;
  }
}

/* ===============================
   Sheet Mapping (FIXED)
================================ */
const sheetMap = {
  Orders: "Orders_Raw",
  Sessions: "Sessions_Raw",
  Calls: "Calls_Raw"
};

/* ===============================
   Load Sheet
================================ */
function loadData() {
  const sheetName = sheetMap[dataView];
  const sheet = workbook.Sheets[sheetName];

  if (!sheet) {
    console.error("Sheet not found:", sheetName);
    return;
  }

  rawData = XLSX.utils.sheet_to_json(sheet);
  console.log(`${dataView} rows loaded:`, rawData.length);

  processData();
}

/* ===============================
   Process Data
================================ */
function processData() {
  let result = {};
  let entityTracker = {};

  rawData.forEach(row => {
    let rawDate, entityId, value = 1;

    if (dataView === "Orders") {
      rawDate = row["Order Date"];
      entityId = String(row["Phone"] || "").replace(/\D/g, "");
      value = Number(row["Amount"]) || 0;
    }

    if (dataView === "Sessions") {
      rawDate = row["Session Date"];
      entityId = row["Device ID"];
    }

    if (dataView === "Calls") {
      rawDate = row["Call Date"];
      entityId = String(row["Phone"] || "").replace(/\D/g, "");
    }

    if (!rawDate || !entityId) return;

    const timeKey = getTimeKey(rawDate);
    const uniqueKey = `${timeKey}_${entityId}`;

    if (entityTracker[uniqueKey]) return;
    entityTracker[uniqueKey] = true;

    result[timeKey] = (result[timeKey] || 0) + value;
  });

  drawChart(result);
}

/* ===============================
   Draw Chart
================================ */
function drawChart(data) {
  const ctx = document.getElementById("chart").getContext("2d");

  if (chartInstance) chartInstance.destroy();

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: Object.keys(data),
      datasets: [{
        label: `${dataView} (${timeGranularity})`,
        data: Object.values(data),
        backgroundColor: "rgba(54,162,235,0.6)"
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}

/* ===============================
   Load Excel LAST
================================ */
fetch("Data Analytics Intern Assignment - Data Set.xlsx")
  .then(res => res.arrayBuffer())
  .then(buffer => {
    workbook = XLSX.read(buffer, { type: "array" });
    console.log("Sheet names:", workbook.SheetNames);
    loadData();
  });

/* ===============================
   Dropdown Listeners
================================ */
document.getElementById("time").addEventListener("change", e => {
  timeGranularity = e.target.value;
  processData();
});

document.getElementById("view").addEventListener("change", e => {
  dataView = e.target.value;
  loadData();
});









