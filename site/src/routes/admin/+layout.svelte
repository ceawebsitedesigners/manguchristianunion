<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { base } from '$app/paths';
    import { goto } from '$app/navigation';

    let theme = 'light';
    let isMounted = false;

    // Check if the current route is the login page (no navbar)
    $: isLogin = $page.url.pathname === `${base}/admin`;

    onMount(() => {
        isMounted = true;
        const stored = localStorage.getItem('adminTheme');
        if (stored) {
            theme = stored;
        } else {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }
        document.documentElement.setAttribute('data-theme', theme);
    });

    function toggleTheme() {
        theme = theme === 'light' ? 'dark' : 'light';
        localStorage.setItem('adminTheme', theme);
        document.documentElement.setAttribute('data-theme', theme);
    }

    function handleLogout() {
        localStorage.removeItem('authToken');
        goto(`${base}/admin`);
    }
</script>

<div class="admin-layout" data-theme={theme} style:visibility={isMounted ? 'visible' : 'hidden'}>
    {#if !isLogin}
        <nav class="navbar">
            <div class="nav-left">
                {#if $page.url.pathname !== `${base}/admin/dashboard`}
                    <a href="{base}/admin/dashboard" class="back-btn">← Back</a>
                {/if}
                <a href="{base}/admin/dashboard" class="navbar-brand">
                    <div class="logo">🙏</div>
                    <div class="brand-text">
                        <h1>Admin Panel</h1>
                        <p>Mangu Christian Union</p>
                    </div>
                </a>
            </div>

            <div class="nav-right">
                <button class="theme-toggle" on:click={toggleTheme} aria-label="Toggle Theme">
                    {#if theme === 'light'}
                        🌙
                    {:else}
                        ☀️
                    {/if}
                </button>
                <button on:click={handleLogout} class="logout-btn">Log Out</button>
            </div>
        </nav>
    {/if}

    <div class="layout-content">
        <slot />
    </div>
</div>

<style>
    /* Global Styles and CSS Variables */
    :global(:root) {
        /* Light Theme (Default) */
        --bg-color: #f4f6f9;
        --bg-gradient: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        --card-bg: #ffffff;
        --card-border: #f1f2f6;
        --card-shadow: rgba(0,0,0,0.06);
        --text-primary: #333333;
        --text-secondary: #7f8c8d;
        --text-muted: #888888;
        --heading-color: #2c3e50;
        
        --input-bg: #fafbfa;
        --input-border: #dddddd;
        --input-focus: rgba(255, 215, 0, 0.15);
        
        --nav-bg: #ffffff;
        --nav-shadow: rgba(0, 0, 0, 0.05);

        --accent-primary: #ffd700;
        --accent-hover: #ffb700;
        --accent-gradient: linear-gradient(135deg, #ffd700, #ffb700);
        --accent-gradient-hover: linear-gradient(135deg, #ffb700, #f39c12);
        --accent-text: #ffffff;
        --accent-shadow: rgba(255, 215, 0, 0.3);

        --success-bg: #e8f8f5;
        --success-text: #27ae60;
        --success-border: #d1f2eb;

        --error-bg: #fdedec;
        --error-text: #c0392b;
        --error-border: #fadbd8;
        
        --btn-disabled: #cccccc;
        --dashed-border: #cccccc;
        --list-item-bg: #fcfcfc;
    }

    :global(:root[data-theme="dark"]) {
        /* Dark Theme */
        --bg-color: #0a0a0a;
        --bg-gradient: #0a0a0a;
        --card-bg: #151515;
        --card-border: #222222;
        --card-shadow: rgba(0,0,0,0.5);
        --text-primary: #e8e8e8;
        --text-secondary: #aaaaaa;
        --text-muted: #666666;
        --heading-color: #f1f1f1;
        
        --input-bg: #111113;
        --input-border: #333333;
        --input-focus: rgba(255, 215, 0, 0.15);
        
        --nav-bg: #151515;
        --nav-shadow: rgba(0, 0, 0, 0.8);

        --accent-primary: #f5e104;
        --accent-hover: #d4c204;
        --accent-gradient: linear-gradient(135deg, #f5e104, #d4c204);
        --accent-gradient-hover: linear-gradient(135deg, #d4c204, #b4a204);
        --accent-text: #050505;
        --accent-shadow: rgba(245, 225, 4, 0.2);

        --success-bg: rgba(74, 222, 128, 0.1);
        --success-text: #4ade80;
        --success-border: rgba(74, 222, 128, 0.2);

        --error-bg: rgba(248, 113, 113, 0.1);
        --error-text: #f87171;
        --error-border: rgba(248, 113, 113, 0.2);
        
        --btn-disabled: #444444;
        --dashed-border: #444444;
        --list-item-bg: #1a1a1c;
    }

    :global(body) {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: var(--bg-gradient);
        background-color: var(--bg-color);
        color: var(--text-primary);
        transition: background-color 0.3s ease, color 0.3s ease, background 0.3s ease;
        overflow-x: hidden;
    }

    .admin-layout {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }

    /* Top Navigation Bar */
    .navbar {
        background-color: var(--nav-bg);
        box-shadow: 0 4px 15px var(--nav-shadow);
        padding: 1rem 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 100;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
    }

    .nav-left {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .back-btn {
        color: var(--text-secondary);
        text-decoration: none;
        font-weight: 600;
        margin-right: 10px;
        transition: color 0.2s;
    }

    .back-btn:hover {
        color: var(--accent-primary);
    }

    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 15px;
        text-decoration: none;
        color: var(--text-primary);
    }

    .logo {
        width: 45px;
        height: 45px;
        background: var(--accent-gradient);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        box-shadow: 0 5px 15px var(--accent-shadow);
        transition: box-shadow 0.3s ease;
    }

    .brand-text h1 { margin: 0; font-size: 20px; font-weight: 700; color: var(--heading-color); }
    .brand-text p { margin: 0; font-size: 13px; color: var(--text-muted); }

    .nav-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .theme-toggle {
        background: none;
        border: none;
        font-size: 20px;
        cursor: pointer;
        padding: 8px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: background 0.2s;
        color: var(--text-primary);
    }

    .theme-toggle:hover {
        background: var(--card-border);
    }

    .logout-btn {
        background-color: var(--error-bg);
        color: var(--error-text);
        border: 1px solid var(--error-border);
        padding: 8px 18px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        text-decoration: none;
    }

    .logout-btn:hover { background-color: var(--error-text); color: white; border-color: var(--error-text); }

    .layout-content {
        flex: 1;
        display: flex;
        flex-direction: column;
    }
</style>
