/**
 * ==========================================================================
 * BioSync Pro - Simplified Dashboard Controller (No Chart.js)
 * ==========================================================================
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Verify Authentication
    const token = localStorage.getItem('jwt_token');
    if (!token) {
        window.location.href = '/login';
        return;
    }

    // 2. Fetch initial data load
    fetchDashboardData();
    fetchLiveVerificationFeed();

    // 3. Set up the Live Polling Loop
    setInterval(fetchLiveVerificationFeed, 3000);
});

async function fetchDashboardData() {
    const token = localStorage.getItem('jwt_token');
    try {
        const response = await fetch('/api/dashboard/stats', {
            method: 'GET',
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401 || response.status === 422) {
            localStorage.removeItem('jwt_token');
            window.location.href = '/login';
            return;
        }

        const data = await response.json();
        
        // Update Metric Cards
        const total = data.total_students || 0;
        const present = data.present_today || 0;
        
        document.getElementById('stat-total-students').innerText = total;
        document.getElementById('stat-present').innerText = present;
        document.getElementById('stat-absent').innerText = data.absent_today || 0;
        
        // Update the Progress Bar visually based on attendance percentage
        let percentage = 0;
        if (total > 0) {
            percentage = Math.round((present / total) * 100);
        }
        
        document.getElementById('ratio-bar').style.width = `${percentage}%`;
        document.getElementById('ratio-text').innerText = `${percentage}%`;

    } catch (err) {
        console.error("Failed to fetch dashboard metrics:", err);
    }
}

async function fetchLiveVerificationFeed() {
    const token = localStorage.getItem('jwt_token');
    try {
        const response = await fetch('/api/attendance/live', {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) throw new Error("Failed to fetch live feed");

        const items = await response.json();
        
        // Build HTML string in memory to prevent screen flicker
        let htmlContent = "";

        if(items.length === 0) {
            htmlContent = `<tr><td colspan="6" class="text-center text-muted py-4">No attendance records for today yet. Waiting for hardware scans...</td></tr>`;
        } else {
            items.forEach(item => {
                htmlContent += `
                    <tr>
                        <td><strong>${item.roll_number}</strong></td>
                        <td>${item.full_name}</td>
                        <td><span class="text-secondary small"><i class="fa-solid fa-building me-1"></i>${item.department}</span></td>
                        <td><i class="fa-regular fa-clock me-1 text-primary"></i> ${item.time}</td>
                        <td><code class="text-secondary small bg-light px-2 py-1 rounded">${item.mac_address}</code></td>
                        <td><span class="badge badge-outline-success px-2 py-1"><i class="fa-solid fa-check me-1"></i>Verified</span></td>
                    </tr>
                `;
            });
        }

        // Inject string instantly
        document.getElementById('live-attendance-feed').innerHTML = htmlContent;

        document.getElementById('stream-status').innerText = "Online";
        document.getElementById('stream-status').className = "badge bg-success";

    } catch (err) {
        console.error("Live feed connection error:", err);
        const statusBadge = document.getElementById('stream-status');
        statusBadge.innerText = "Connection Lost";
        statusBadge.className = "badge bg-danger";
    }
}