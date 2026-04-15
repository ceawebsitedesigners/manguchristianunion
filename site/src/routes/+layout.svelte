<script lang="ts">
	import favicon from '$lib/assets/hero-church.jpg';
	

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>


{@render children()}



