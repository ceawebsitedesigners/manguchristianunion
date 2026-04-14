<script lang="ts">
    import { base } from '$app/paths';
    import { URLS } from '$lib/urls';
    import { clearLeadershipCache } from '$lib/stores';

    let year = new Date().getFullYear();
    let theme = '';

    // Simple fields
    let singleFields: Record<string, string> = {
        chairman: '', deputyChairman: '', treasurer: '', secretary: '',
        prayerCoordinator: '', choirMaster: '', assistantChoirMaster: '',
        talentsCoordinator: '', assistantTalentsCoordinator: ''
    };

    // Array fields with initial empty items
    let arrayFields: Record<string, string[]> = {
        assistantPrayerCoordinators: [''], childrensMinistry: [''],
        churchCoordinators: [''], followUpCoordinators: [''],
        believersCoordinators: [''], assistantBelieversCoordinators: [''],
        royalPriesthood: [''], engineers: [''],
        praiseAndWorshipCoordinators: [''], bibleStudyCoordinators: ['']
    };

    let isSubmitting = false;
    let messageType = ''; // 'success' | 'error' | ''
    let messageText = '';

    function addArrayItem(fieldKey: string) {
        arrayFields[fieldKey] = [...arrayFields[fieldKey], ''];
    }

    function removeArrayItem(fieldKey: string, index: number) {
        arrayFields[fieldKey] = arrayFields[fieldKey].filter((_, i) => i !== index);
        // Ensure there's always at least one input available
        if (arrayFields[fieldKey].length === 0) {
            arrayFields[fieldKey] = [''];
        }
    }

    async function handleSubmit() {
        isSubmitting = true;
        messageType = '';
        messageText = '';

        try {
            // Reconstruct payload dynamically
            const payload: any = { year, theme, leaders: {} };

            // Check single fields
            for (const [key, val] of Object.entries(singleFields)) {
                if (val.trim() !== '') {
                    payload.leaders[key] = val.trim();
                }
            }

            // Check array fields
            for (const [key, vals] of Object.entries(arrayFields)) {
                const cleaned = vals.map(v => v.trim()).filter(v => v !== '');
                if (cleaned.length > 0) {
                    payload.leaders[key] = cleaned;
                }
            }

            const response = await fetch(URLS.leadership, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                messageType = 'success';
                messageText = 'Leadership data saved successfully!';
                clearLeadershipCache();
            } else {
                const errorText = await response.text();
                messageType = 'error';
                messageText = `Error: ${errorText}`;
            }

        } catch (err) {
            console.error(err);
            messageType = 'error';
            messageText = 'Connection error. Make sure the API is running.';
        } finally {
            isSubmitting = false;
        }
    }

    // A helper utility to format label text
    function formatLabel(key: string) {
        const result = key.replace(/([A-Z])/g, " $1");
        return result.charAt(0).toUpperCase() + result.slice(1);
    }
</script>

<svelte:head>
    <title>Add Leaders - Mangu CU</title>
</svelte:head>



<div class="container">
    <div class="form-card">
        <div class="form-header">
            <h2>Add / Update Leaders</h2>
            <p>Register the church officials for a specific academic year</p>
        </div>

        <form on:submit|preventDefault={handleSubmit}>
            <!-- Section: Base -->
            <div class="form-section">
                <div class="form-section-title">📍 General Information</div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="year">Year</label>
                        <input type="number" id="year" bind:value={year} required placeholder="e.g. 2024">
                    </div>
                    <div class="form-group">
                        <label for="theme">Annual Theme</label>
                        <input type="text" id="theme" bind:value={theme} required placeholder="e.g. Walking in the Light">
                    </div>
                </div>
            </div>

            <!-- Section: Executive -->
            <div class="form-section">
                <div class="form-section-title">⭐ Executive Board</div>
                <div class="form-row">
                    {#each ['chairman', 'deputyChairman', 'treasurer', 'secretary'] as field}
                        <div class="form-group">
                            <label>{formatLabel(field)}</label>
                            <input type="text" bind:value={singleFields[field]} placeholder="Full Name" required>
                        </div>
                    {/each}
                </div>
            </div>

            <!-- Section: Departments (Single Roles) -->
            <div class="form-section">
                <div class="form-section-title">🏛️ Department Heads (Singular)</div>
                <div class="form-row">
                    {#each ['prayerCoordinator', 'choirMaster', 'assistantChoirMaster', 'talentsCoordinator', 'assistantTalentsCoordinator'] as field}
                        <div class="form-group">
                            <label>{formatLabel(field)}</label>
                            <input type="text" bind:value={singleFields[field]} placeholder="Full Name">
                        </div>
                    {/each}
                </div>
            </div>

            <!-- Section: Departments (Groups/Arrays) -->
            <div class="form-section">
                <div class="form-section-title">👥 Team Roles (Multiple People)</div>
                <div class="form-row">
                    {#each Object.keys(arrayFields) as fieldKey}
                        <div class="form-group">
                            <label>{formatLabel(fieldKey)}</label>
                            <div class="dynamic-list">
                                {#each arrayFields[fieldKey] as item, index}
                                    <div class="dynamic-item">
                                        <input type="text" bind:value={arrayFields[fieldKey][index]} placeholder="Full Name">
                                        <button type="button" class="btn-remove" on:click={() => removeArrayItem(fieldKey, index)}>×</button>
                                    </div>
                                {/each}
                                <button type="button" class="btn-add" on:click={() => addArrayItem(fieldKey)}>+ Add Official</button>
                            </div>
                        </div>
                    {/each}
                </div>
            </div>

            {#if messageType}
                <div class="message {messageType}">{messageText}</div>
            {/if}

            <button type="submit" class="submit-btn" disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Save Leadership Data'}
            </button>
        </form>
    </div>
</div>

<style>
    /* Form Container */
    .container { max-width: 900px; margin: 3rem auto; padding: 0 20px; }
    .form-card { background: var(--card-bg); border-radius: 16px; box-shadow: 0 8px 30px var(--card-shadow); padding: 40px; border: 1px solid var(--card-border); }
    .form-header { margin-bottom: 30px; border-bottom: 2px solid var(--border-color); padding-bottom: 20px; }
    .form-header h2 { margin: 0; font-size: 2rem; color: var(--heading-color); font-weight: 700; }
    .form-header p { margin: 5px 0 0; color: var(--text-secondary); font-size: 1.05rem; }

    /* Form Layout */
    .form-section { margin-bottom: 35px; }
    .form-section-title { font-size: 1.3rem; color: var(--accent-primary); margin-bottom: 20px; font-weight: 600; display: flex; align-items: center; gap: 10px; }
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
    .form-group { display: flex; flex-direction: column; gap: 8px; }

    label { font-weight: 600; font-size: 0.9rem; color: var(--heading-color); }
    input[type="text"], input[type="number"] { width: 100%; padding: 12px 15px; border: 1px solid var(--input-border); border-radius: 8px; font-size: 1rem; color: var(--text-primary); transition: all 0.3s ease; background-color: var(--input-bg); box-sizing: border-box;}
    input:focus { outline: none; border-color: var(--accent-primary); box-shadow: 0 0 0 3px var(--input-focus); background-color: var(--card-bg); }

    /* Dynamic List Area */
    .dynamic-list { display: flex; flex-direction: column; gap: 12px; background: var(--list-item-bg); padding: 15px; border-radius: 8px; border: 1px dashed var(--dashed-border); }
    .dynamic-item { display: flex; gap: 10px; align-items: center; }
    .dynamic-item input { flex: 1; min-width: 0; }
    .btn-remove { background: var(--error-bg); color: var(--error-text); border: none; border-radius: 6px; width: 36px; height: 36px; font-weight: bold; cursor: pointer; transition: 0.2s; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
    .btn-remove:hover { background: var(--error-text); color: white; }
    .btn-add { background: none; color: #2e86de; border: 1px dashed #2e86de; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; transition: 0.2s; margin-top: 5px; }
    .btn-add:hover { background: rgba(46, 134, 222, 0.1); }

    /* Submit Button */
    .submit-btn { background: var(--accent-gradient); color: var(--accent-text); border: none; padding: 16px; border-radius: 10px; font-size: 1.1rem; font-weight: 700; width: 100%; cursor: pointer; transition: all 0.3s; margin-top: 20px; box-shadow: 0 6px 20px var(--accent-shadow); }
    .submit-btn:hover:not(:disabled) { transform: translateY(-2px); background: var(--accent-gradient-hover); box-shadow: 0 10px 25px var(--accent-shadow); }
    .submit-btn:disabled { background: var(--btn-disabled); cursor: not-allowed; box-shadow: none; transform: none; color: white;}

    .message { margin-top: 15px; padding: 12px; border-radius: 8px; font-weight: 500; text-align: center; }
    .message.success { background-color: var(--success-bg); color: var(--success-text); border: 1px solid var(--success-border); }
    .message.error { background-color: var(--error-bg); color: var(--error-text); border: 1px solid var(--error-border); }

    @media (max-width: 768px) {
        .form-row { grid-template-columns: 1fr; gap: 15px; }
        .form-card { padding: 25px; }
    }
</style>
