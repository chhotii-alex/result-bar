<script>
  import FancyFieldset from "./FancyFieldset.svelte";

  export let quantTestList;
  export let testList;
  export let selectedDx;

  let formOpen = false;
</script>

<FancyFieldset bind:exploreGroupsOpen={formOpen} label="Pick Laboratory Test">
  <div class="buttons">
    {#if quantTestList}
      <span><strong>Quantitative</strong></span><br />
      {#each quantTestList as dx}
        <span>
          <input type="radio" id={dx} value={dx} bind:group={selectedDx} />
          <label for={dx}> {dx} </label>
        </span>
        <br />
      {/each}
    {/if}
    {#if testList}
      <span><strong>Positive/Negative</strong></span><br />
      {#each testList as dx}
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
  @media only screen and (max-width: 850px) {
    div.buttons {
      columns: 1;
    }
  }
</style>
