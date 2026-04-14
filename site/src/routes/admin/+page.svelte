<script lang="ts">
    import { goto } from '$app/navigation';
    import { base } from '$app/paths';
    import { onMount } from 'svelte';

    let username = '';
    let password = '';
    let rememberMe = false;
    let isLoading = false;
    let errorMessage = '';
    let successMessage = '';
    const app_id = "mangucu5202ekkmrk6022"

    onMount(() => {
        // If already logged in, fast-forward to dashboard
        if (localStorage.getItem('authToken')) {
            goto(`${base}/admin/dashboard`);
        }
    });

    async function handleLogin() {
        if (!username || !password) {
            errorMessage = 'Please fill in all fields';
            return;
        }

        isLoading = true;
        errorMessage = '';
        successMessage = '';

        try {
            const response = await fetch('https://global-processes.onrender.com/auth/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username,
                    password,
                    rememberMe,
                    app_id
                })
            });

            if (response.ok) {
                const data = await response.json();
                successMessage = 'Login successful! Redirecting...';
                
                if (data.token) {
                    localStorage.setItem('authToken', data.token);
                }

                setTimeout(() => {
                    if (data.redirectUrl) {
                        window.location.href = data.redirectUrl;
                    } else {
                        goto(`${base}/admin/dashboard`);
                    }
                }, 500);
            } else {
                const errorData = await response.json();
                errorMessage = errorData.message || 'Login failed. Please check your credentials.';
            }
        } catch (error) {
            errorMessage = 'An error occurred. Please try again later.';
        } finally {
            isLoading = false;
        }
    }
</script>

<svelte:head>
    <title>Mangu Cu Admin</title>
</svelte:head>

<div class="container-wrapper">
    <div class="container">
        <div class="login-card">
            <div class="header">
                <div class="logo">🙏</div>
                <h1 class="title">Admin Login</h1>
                <p class="subtitle">Mangu Christian Union</p>
            </div>

            <!-- Messages -->
            {#if errorMessage}
                <div class="message error-message">{errorMessage}</div>
            {/if}
            {#if successMessage}
                <div class="message success-message">{successMessage}</div>
            {/if}

            <form on:submit|preventDefault={handleLogin}>
                <div class="form-group">
                    <label class="form-label" for="username">Username</label>
                    <input 
                        type="text" 
                        id="username" 
                        class="form-input" 
                        placeholder="Enter your username"
                        bind:value={username}
                        required
                    >
                </div>

                <div class="form-group">
                    <label class="form-label" for="password">Password</label>
                    <input 
                        type="password" 
                        id="password" 
                        class="form-input" 
                        placeholder="Enter your password"
                        bind:value={password}
                        required
                    >
                </div>

                
                <button type="submit" class="login-btn" disabled={isLoading}>
                    {isLoading ? 'Logging in...' : 'Login'}
                </button>
            </form>

            
        </div>
    </div>
</div>

<style>
    .container-wrapper {
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: var(--bg-gradient);
        position: relative;
        overflow: hidden;
    }

    .container-wrapper::before {
        content: '';
        position: absolute;
        width: 400px;
        height: 400px;
        background: var(--accent-shadow);
        border-radius: 50%;
        top: -100px;
        left: -100px;
        animation: float 6s ease-in-out infinite;
    }

    .container-wrapper::after {
        content: '';
        position: absolute;
        width: 300px;
        height: 300px;
        background: var(--accent-shadow);
        border-radius: 50%;
        bottom: -150px;
        right: -150px;
        animation: float 8s ease-in-out infinite reverse;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(30px); }
    }

    .container {
        width: 100%;
        max-width: 450px;
        padding: 20px;
        position: relative;
        z-index: 1;
    }

    .login-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 20px;
        box-shadow: 0 20px 60px var(--card-shadow);
        padding: 50px 40px;
        animation: slideUp 0.6s ease-out;
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .header {
        text-align: center;
        margin-bottom: 40px;
    }

    .logo {
        width: 80px;
        height: 80px;
        margin: 0 auto 20px;
        background: var(--accent-gradient);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        box-shadow: 0 10px 30px var(--accent-shadow);
        animation: bounce 2s ease-in-out infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .title {
        color: var(--heading-color);
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .subtitle {
        color: var(--text-secondary);
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    .form-group {
        margin-bottom: 20px;
    }

    .form-label {
        display: block;
        color: var(--heading-color);
        font-weight: 600;
        margin-bottom: 8px;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .form-input {
        width: 100%;
        padding: 14px 16px;
        border: 2px solid var(--input-border);
        border-radius: 10px;
        font-size: 16px;
        color: var(--text-primary);
        transition: all 0.3s ease;
        background: var(--input-bg);
        box-sizing: border-box;
    }

    .form-input:focus {
        outline: none;
        border-color: var(--accent-primary);
        background: var(--card-bg);
        box-shadow: 0 0 0 4px var(--input-focus);
    }

    .form-input::placeholder {
        color: var(--text-muted);
    }

    .login-btn {
        width: 100%;
        padding: 14px;
        background: var(--accent-gradient);
        border: none;
        border-radius: 10px;
        color: var(--accent-text);
        font-size: 16px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 10px 25px var(--accent-shadow);
    }

    .login-btn:hover:not(:disabled) {
        background: var(--accent-gradient-hover);
        transform: translateY(-2px);
        box-shadow: 0 15px 35px var(--accent-shadow);
    }

    .login-btn:active:not(:disabled) {
        transform: translateY(0);
    }
    
    .login-btn:disabled {
        opacity: 0.7;
        cursor: not-allowed;
    }

    .message {
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 14px;
        font-weight: 500;
        animation: slideDown 0.3s ease-out;
    }

    .error-message {
        background-color: var(--error-bg);
        color: var(--error-text);
        border: 1px solid var(--error-border);
    }

    .success-message {
        background-color: var(--success-bg);
        color: var(--success-text);
        border: 1px solid var(--success-border);
    }

    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 480px) {
        .login-card { padding: 40px 25px; }
        .title { font-size: 24px; }
    }
</style>
