<script>
  let { data } = $props();
</script>

<main
  class="relative flex flex-col items-center justify-center min-h-screen py-10"
>
<ul>
  {#each data.jellies as jelly}
    <li>{jelly.name}</li>
  {/each}
</ul>
  <div class="flex flex-col items-center grow">
    <a
      href="https://github.com/le2310al/jellydrop"
      class="flex items-center h-8 mt-auto space-x-2 bottom-20 right-20"
    >
      <img src="/github.svg" alt="GitHub Logo" class="h-6 dark:invert" />
      <p class="font-light">Source</p>
    </a>
  </div>
</main>
