let map;
let markerLayer;
let allDistrictsAndAreas = {};

document.addEventListener("DOMContentLoaded", () => {
  initMap();
  loadStats();
  loadDistrictsAndAreas();
  loadBusinesses();
  setupEventListeners();
});

function initMap() {
  // Center of Dar es Salaam
  map = L.map("map").setView([-6.814, 39.245], 11);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  markerLayer = L.layerGroup().addTo(map);
}

async function loadStats() {
  try {
    const res = await fetch("/api/stats");
    const data = await res.json();
    document.getElementById("statTotal").textContent = data.total_verified || 0;
    document.getElementById("statAgrovet").textContent = data.total_agrovet || 0;
    document.getElementById("statVet").textContent = data.total_veterinary || 0;
    document.getElementById("statFeed").textContent = data.total_feed_poultry || 0;
    document.getElementById("statReview").textContent = data.total_needs_review || 0;
  } catch (err) {
    console.error("Failed to load stats:", err);
  }
}

async function loadDistrictsAndAreas() {
  try {
    const res = await fetch("/api/districts-and-areas");
    allDistrictsAndAreas = await res.json();
    updateAreaDropdown("ALL");
  } catch (err) {
    console.error("Failed to load districts & areas:", err);
  }
}

function updateAreaDropdown(selectedDistrict) {
  const areaSelect = document.getElementById("filterArea");
  areaSelect.innerHTML = '<option value="ALL">All Areas</option>';

  let areas = [];
  if (selectedDistrict === "ALL") {
    // Collect all areas across all districts
    Object.values(allDistrictsAndAreas).forEach(arr => {
      areas = areas.concat(arr);
    });
  } else if (allDistrictsAndAreas[selectedDistrict]) {
    areas = allDistrictsAndAreas[selectedDistrict];
  }

  // Deduplicate and sort
  const uniqueAreas = Array.from(new Set(areas)).sort();
  uniqueAreas.forEach(a => {
    const opt = document.createElement("option");
    opt.value = a;
    opt.textContent = a;
    areaSelect.appendChild(opt);
  });
}

async function loadBusinesses() {
  const search = document.getElementById("searchInput").value.trim();
  const district = document.getElementById("filterDistrict").value;
  const area = document.getElementById("filterArea").value;
  const clusterEl = document.getElementById("filterCluster");
  const cluster = clusterEl ? clusterEl.value : "ALL";
  const category = document.getElementById("filterCategory").value;
  const status = document.getElementById("filterStatus").value;

  const params = new URLSearchParams();
  if (search) params.append("search", search);
  if (district !== "ALL") params.append("district", district);
  if (area !== "ALL") params.append("area", area);
  if (cluster !== "ALL") params.append("cluster", cluster);
  if (category !== "ALL") params.append("category", category);
  if (status !== "ALL") params.append("status", status);

  try {
    const res = await fetch(`/api/businesses?${params.toString()}`);
    const data = await res.json();
    renderBusinesses(data.items || []);
  } catch (err) {
    console.error("Failed to load businesses:", err);
  }
}

function getCategoryColor(category) {
  switch (category) {
    case "AGROVET": return "#15803d"; // Green
    case "VETERINARY_SHOP":
    case "VETERINARY_PHARMACY":
    case "VETERINARY_SERVICE": return "#0284c7"; // Blue
    case "ANIMAL_FEED": return "#d97706"; // Amber
    case "POULTRY_FEED":
    case "POULTRY_SUPPLIES": return "#7e22ce"; // Purple
    default: return "#475569"; // Gray
  }
}

function getCategoryBadgeClass(category) {
  if (category === "AGROVET") return "cat-agrovet";
  if (category.startsWith("VET")) return "cat-vet";
  if (category === "ANIMAL_FEED") return "cat-feed";
  if (category.startsWith("POULTRY")) return "cat-poultry";
  return "cat-other";
}

function renderBusinesses(items) {
  document.getElementById("resultCount").textContent = `${items.length} found`;
  document.getElementById("mapMarkerCount").textContent = `${items.filter(b => b.latitude && b.longitude).length} pins`;

  const cardsContainer = document.getElementById("cardsList");
  cardsContainer.innerHTML = "";
  markerLayer.clearLayers();

  if (items.length === 0) {
    cardsContainer.innerHTML = `<div style="text-align: center; padding: 40px; color: #64748b;">No businesses match the selected filters.</div>`;
    return;
  }

  const mapBounds = [];

  items.forEach(biz => {
    // 1. Create Business Card
    const card = document.createElement("div");
    card.className = "business-card";

    const badgeClass = getCategoryBadgeClass(biz.category);
    const phoneDisplay = biz.phone ? `<a href="tel:${biz.phone.replace(/\s+/g, '')}" class="contact-item">📞 ${biz.phone}</a>` : `<span style="color:#94a3b8;font-size:12px;">No phone listed</span>`;
    const altPhoneDisplay = biz.alternative_phone ? `<a href="tel:${biz.alternative_phone.replace(/\s+/g, '')}" class="contact-item">📞 ${biz.alternative_phone}</a>` : '';
    const gmapsBtn = biz.google_maps_url ? `<a href="${biz.google_maps_url}" target="_blank" class="btn-gmaps">📍 Open in Google Maps</a>` : '';

    const sources = (biz.source_types || []).join(", ");

    card.innerHTML = `
      <div class="card-header">
        <div>
          <div class="card-title">${biz.business_name}</div>
          <div class="card-location">📍 ${biz.ward_or_area || 'UNKNOWN'} &bull; ${biz.district || 'UNKNOWN'} ${biz.hotspot_cluster && biz.hotspot_cluster !== 'GENERAL_METROPOLITAN' ? `&bull; <span style="color:#b45309;font-weight:600;">⚡ ${biz.hotspot_cluster}</span>` : ''}</div>
        </div>
        <div class="card-badges">
          <span class="cat-badge ${badgeClass}">${biz.category}</span>
          <span class="badge" style="font-size:10px;">${biz.confidence}</span>
        </div>
      </div>

      ${biz.street_or_address ? `<div class="card-address">${biz.street_or_address}</div>` : ''}

      <div class="card-contact">
        ${phoneDisplay}
        ${altPhoneDisplay}
      </div>

      <div class="card-footer">
        <div class="card-evidence" title="${biz.evidence || ''}">
          🔍 ${biz.evidence || 'Public registration listing'}
        </div>
        <div>
          ${gmapsBtn}
        </div>
      </div>
    `;

    cardsContainer.appendChild(card);

    // 2. Add to Map if coordinates exist
    if (biz.latitude && biz.longitude) {
      const lat = parseFloat(biz.latitude);
      const lon = parseFloat(biz.longitude);

      if (!isNaN(lat) && !isNaN(lon)) {
        mapBounds.push([lat, lon]);
        const circleMarker = L.circleMarker([lat, lon], {
          radius: 7,
          fillColor: getCategoryColor(biz.category),
          color: "#ffffff",
          weight: 2,
          opacity: 1,
          fillOpacity: 0.85
        });

        const popupContent = `
          <div style="font-family: 'Inter', sans-serif; font-size: 13px;">
            <strong style="font-size: 14px; color: #0f172a;">${biz.business_name}</strong><br>
            <span style="font-size: 11px; font-weight: 700; color: ${getCategoryColor(biz.category)};">${biz.category}</span><br>
            <span style="color: #64748b;">${biz.ward_or_area || ''}, ${biz.district || ''}</span><br>
            ${biz.hotspot_cluster && biz.hotspot_cluster !== 'GENERAL_METROPOLITAN' ? `<span style="font-size: 11px; color: #b45309; font-weight: 600;">⚡ ${biz.hotspot_cluster}</span><br>` : ''}
            ${biz.street_or_address ? `<span style="font-size: 11px;">${biz.street_or_address}</span><br>` : ''}
            ${biz.phone ? `<strong>Tel:</strong> <a href="tel:${biz.phone}">${biz.phone}</a><br>` : ''}
            <div style="margin-top: 8px;">
              <a href="${biz.google_maps_url}" target="_blank" style="display:inline-block; padding: 4px 8px; background: #1e3a8a; color: #fff; text-decoration: none; border-radius: 4px; font-size: 11px; font-weight: 600;">
                Open in Google Maps &rarr;
              </a>
            </div>
          </div>
        `;
        circleMarker.bindPopup(popupContent);
        markerLayer.addLayer(circleMarker);
      }
    }
  });

  // Fit map to bounds if markers exist
  if (mapBounds.length > 0) {
    map.fitBounds(mapBounds, { padding: [30, 30], maxZoom: 14 });
  }
}

function setupEventListeners() {
  let debounceTimeout;
  document.getElementById("searchInput").addEventListener("input", () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      loadBusinesses();
    }, 300);
  });

  document.getElementById("filterDistrict").addEventListener("change", (e) => {
    updateAreaDropdown(e.target.value);
    loadBusinesses();
  });

  document.getElementById("filterArea").addEventListener("change", () => {
    loadBusinesses();
  });

  const filterCluster = document.getElementById("filterCluster");
  if (filterCluster) {
    filterCluster.addEventListener("change", () => {
      loadBusinesses();
    });
  }

  document.getElementById("filterCategory").addEventListener("change", () => {
    loadBusinesses();
  });

  document.getElementById("filterStatus").addEventListener("change", () => {
    loadBusinesses();
  });

  document.getElementById("btnResetFilters").addEventListener("click", () => {
    document.getElementById("searchInput").value = "";
    document.getElementById("filterDistrict").value = "ALL";
    updateAreaDropdown("ALL");
    const clusterEl = document.getElementById("filterCluster");
    if (clusterEl) clusterEl.value = "ALL";
    document.getElementById("filterCategory").value = "ALL";
    document.getElementById("filterStatus").value = "VERIFIED";
    loadBusinesses();
  });

  document.getElementById("btnExportCsv").addEventListener("click", () => {
    const search = document.getElementById("searchInput").value.trim();
    const district = document.getElementById("filterDistrict").value;
    const area = document.getElementById("filterArea").value;
    const clusterEl = document.getElementById("filterCluster");
    const cluster = clusterEl ? clusterEl.value : "ALL";
    const category = document.getElementById("filterCategory").value;
    const status = document.getElementById("filterStatus").value;

    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (district !== "ALL") params.append("district", district);
    if (area !== "ALL") params.append("area", area);
    if (cluster !== "ALL") params.append("cluster", cluster);
    if (category !== "ALL") params.append("category", category);
    if (status !== "ALL") params.append("status", status);

    window.location.href = `/api/export/csv?${params.toString()}`;
  });
}