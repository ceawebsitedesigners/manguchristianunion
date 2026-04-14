<script lang="ts">
    import { goto } from '$app/navigation';
    import { base } from '$app/paths';
    import { onMount } from 'svelte';

    let isCheckingAuth = true;

    onMount(() => {
        // Simple auth check
        const token = localStorage.getItem('authToken');
        // Uncomment to enforce auth strictly:
        // if (!token) { goto(`${base}/admin`); }
        
        setTimeout(() => {
            isCheckingAuth = false;
        }, 300);
    });

    function handleLogout() {
        localStorage.removeItem('authToken');
        goto(`${base}/admin`);
    }
</script>

<svelte:head>
    <title>Admin Dashboard - Mangu CU</title>
</svelte:head>

{#if isCheckingAuth}
    <div id="loader">
        <div class="spinner"></div>
    </div>
{/if}



<!-- Main Content -->
<div class="container">
    <div class="page-header">
        <h2>Welcome to your Dashboard</h2>
        <p>Select what you would like to manage</p>
    </div>

    <div class="dashboard-grid">
        <!-- Upload Photos Card -->
        <a href="{base}/admin/upload" class="card">
            <div class="card-icon">📸</div>
            <h3 class="card-title">Upload Photos</h3>
            <p class="card-desc">Add new event photos and gallery images to keep the website media up to date.</p>
            <div class="card-btn">Manage Photos</div>
        </a>

        <!-- Manage Leadership Card -->
        <a href="{base}/admin/leadership" class="card">
            <div class="card-icon">👥</div>
            <h3 class="card-title">Add Leaders</h3>
            <p class="card-desc">Update the church officials, set yearly themes, and assign roles for the serving term.</p>
            <div class="card-btn">Manage Leaders</div>
        </a>
        
        <!-- Manage Events Card -->
        <a href="{base}/admin/events" class="card">
            <div class="card-icon">📅</div>
            <h3 class="card-title">Manage Events</h3>
            <p class="card-desc">Add upcoming church events to keep the community informed.</p>
            <div class="card-btn">Manage Events</div>
        </a>

         <!-- Settings Card -->
         <a href="#" class="card" on:click|preventDefault={() => alert('Settings module coming soon!')}>
            <div class="card-icon">⚙️</div>
            <h3 class="card-title">Site Settings</h3>
            <p class="card-desc">Configure general site settings and other miscellaneous options.</p>
            <div class="card-btn">Go to Settings</div>
        </a>
    </div>
</div>


<style>
    /* Main Container */
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 3rem 20px;
    }

    .page-header { margin-bottom: 2.5rem; text-align: center; }
    .page-header h2 { font-size: 2.5rem; color: var(--heading-color); font-weight: 800; margin-bottom: 10px; margin-top: 0; }
    .page-header p { font-size: 1.1rem; color: var(--text-secondary); margin: 0; }

    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }

    /* Dashboard Cards */
    .card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 35px 30px;
        text-align: center;
        box-shadow: 0 10px 30px var(--card-shadow);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        text-decoration: none;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 15px;
        border: 1px solid var(--card-border);
        position: relative;
        overflow: hidden;
    }

    .card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; width: 100%; height: 4px;
        background: var(--accent-gradient);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }

    .card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px var(--card-shadow); border-color: var(--card-border); }
    .card:hover::before { transform: scaleX(1); }

    .card-icon {
        width: 80px; height: 80px;
        background: rgba(255, 215, 0, 0.1); border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 35px; color: #d4a017;
        margin-bottom: 10px; box-shadow: 0 8px 20px var(--accent-shadow);
    }

    .card-title { margin: 0; font-size: 1.6rem; font-weight: 700; color: var(--heading-color); }
    .card-desc { margin: 0; font-size: 1.05rem; color: var(--text-secondary); line-height: 1.5; }

    .card-btn {
        margin-top: 15px; padding: 10px 25px;
        background: var(--accent-gradient); color: var(--accent-text);
        border: none; border-radius: 25px; font-weight: 700; font-size: 0.95rem;
        cursor: pointer; box-shadow: 0 5px 15px var(--accent-shadow);
        transition: all 0.2s ease; text-transform: uppercase; letter-spacing: 0.5px;
    }

    .card:hover .card-btn { background: var(--accent-gradient-hover); transform: scale(1.05); }

    /* Loading Screen */
    #loader {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: white; z-index: 9999; display: flex; justify-content: center; align-items: center;
    }
    .spinner {
        width: 50px; height: 50px; border: 5px solid #f3f3f3;
        border-top: 5px solid #ffd700; border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

    @media (max-width: 768px) {
        .page-header h2 { font-size: 2rem; }
        .dashboard-grid { grid-template-columns: 1fr; }
    }
</style>
