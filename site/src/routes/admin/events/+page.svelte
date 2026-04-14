<script lang="ts">
    import { base } from '$app/paths';
    import { URLS } from '$lib/urls';
    import { clearEventsCache } from '$lib/stores';

    let eventname = '';
    let eventdate = '';
    let eventlocation = '';

    let isSubmitting = false;
    let messageType = ''; // 'success' | 'error' | ''
    let messageText = '';

    async function handleSubmit() {
        isSubmitting = true;
        messageType = '';
        messageText = '';

        try {
            const payload = {
                eventname: eventname.trim(),
                eventdate: eventdate.trim(),
                eventlocation: eventlocation.trim()
            };

            const response = await fetch(URLS.events, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                messageType = 'success';
                messageText = 'Event added successfully!';
                eventname = '';
                eventdate = '';
                eventlocation = '';
                clearEventsCache();
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
</script>

<svelte:head>
    <title>Add Events - Mangu CU</title>
</svelte:head>



<div class="container">
    <div class="form-card">
        <div class="form-header">
            <h2>Add Upcoming Event</h2>
            <p>Publish an upcoming event to the community</p>
        </div>

        <form on:submit|preventDefault={handleSubmit}>
            <div class="form-section">
                <div class="form-section-title">📍 Event Details</div>
                <div class="form-group">
                    <label for="eventname">Event Name</label>
                    <input type="text" id="eventname" bind:value={eventname} required placeholder="e.g. Sunday Service">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label for="eventdate">Event Date</label>
                        <input type="date" id="eventdate" bind:value={eventdate} required>
                    </div>
                    <div class="form-group">
                        <label for="eventlocation">Location</label>
                        <input type="text" id="eventlocation" bind:value={eventlocation} required placeholder="e.g. Main Sanctuary">
                    </div>
                </div>
            </div>

            {#if messageType}
                <div class="message {messageType}">{messageText}</div>
            {/if}

            <button type="submit" class="submit-btn" disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Publish Event'}
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
    .form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px; }
    .form-group { display: flex; flex-direction: column; gap: 8px; margin-bottom: 15px; }

    label { font-weight: 600; font-size: 0.9rem; color: var(--heading-color); }
    input[type="text"], input[type="date"] { width: 100%; padding: 12px 15px; border: 1px solid var(--input-border); border-radius: 8px; font-size: 1rem; color: var(--text-primary); transition: all 0.3s ease; background-color: var(--input-bg); box-sizing: border-box;}
    input:focus { outline: none; border-color: var(--accent-primary); box-shadow: 0 0 0 3px var(--input-focus); background-color: var(--card-bg); }

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
