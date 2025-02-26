<script>
  import FancyFieldset from "./FancyFieldset.svelte";
  export let variablesDataStructure;

  function resetChecks() {
    for (let item of variablesDataStructure.items) {
      item.checked = false;
    }
    variablesDataStructure = variablesDataStructure;
  }

  let exploreGroupsOpen = false;
</script>

<FancyFieldset bind:exploreGroupsOpen label="Explore Groups">
  <div class="controls">
    <div id="select_var_checks">
      <strong>Group</strong>
      <button id="resetChecks" class="bluebutton" on:click={resetChecks}
        >Reset</button
      >
    </div>
    {#if variablesDataStructure}
      {#each variablesDataStructure.items as item (item.id)}
        <div class="group_variable_div">
          <input
            type="checkbox"
            id={item.id}
            class="variablename"
            bind:checked={item.checked}
          />
          <label for={item.id} class="variablename">
            {item.displayName}
          </label>
          <br />
          {#each item.splits as subItem (subItem.value)}
            <input
              type="checkbox"
              id={subItem.value}
              class="valuename"
              bind:checked={subItem.checked}
            />
            <label for={subItem.value} class="valuename">
              {subItem.valueDisplayName}
            </label>
            <br />
          {/each}
        </div>
      {/each}
    {/if}
  </div>
</FancyFieldset>

<style>
  .pick_group_padding {
    padding-left: 70px;
    padding-right: 70px;
  }
  @media only screen and (max-width: 600px) {
    .pick_group_padding {
      padding-left: 30px;
      padding-right: 0px;
    }
  }
  .group_variable_div {
    break-inside: avoid;
  }

  div.controls {
    columns: 4;
  }
</style>
