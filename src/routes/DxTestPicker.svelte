<script>
  import FancyFieldset from "./FancyFieldset.svelte";

  export let dxList;
  export let selectedDx;

  let formOpen = false;
</script>

<FancyFieldset bind:exploreGroupsOpen={formOpen} label="Pick Laboratory Test">
  <div class="buttons">
    {#if dxList}
      {#each dxList as dx}
        <span>
          <input type="radio" id={dx} value={dx} bind:group={selectedDx} />
          <label for={dx}> {dx} </label>
        </span>
        <br />
      {/each}
    {/if}
  </div>
</FancyFieldset>

<style>
  span {
    break-inside: avoid-column;
    break-after: auto;
  }

  div.buttons {
    break-inside: auto;
    columns: 3;
  }
</style>
