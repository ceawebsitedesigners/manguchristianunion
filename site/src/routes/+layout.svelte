<script lang="ts">
	import favicon from '$lib/assets/hero-church.jpg';
	import Nav from '$lib/components/navbar.svelte'

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>


{@render children()}



