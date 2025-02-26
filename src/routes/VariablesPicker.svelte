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

  /* re-order variables */
  function drag(ev) {
    let id = ev.target.id.substring(4);
    ev.dataTransfer.setData("text", id);
  }

  function allowDrop(ev) {
    ev.preventDefault();
  }

  function drop(ev) {
    ev.preventDefault();
    let fromID = ev.dataTransfer.getData("text");
    let target = ev.target;
    while (!target.id || target.tagName != "DIV") {
      target = target.parentElement;
      if (!target) {
        return;
      }
    }
    let toID = target.id.substring(4);
    if (toID == fromID) return;
    swap(toID, fromID);
  }

  function swap(toID, fromID) {
    let toIndex = variablesDataStructure.items.findIndex((t) => t.id == toID);
    if (toIndex < 0) return;
    let fromIndex = variablesDataStructure.items.findIndex(
      (t) => t.id == fromID
    );
    if (fromIndex < 0) return;
    let movedItem = variablesDataStructure.items.splice(fromIndex, 1)[0];
    variablesDataStructure.items.splice(toIndex, 0, movedItem);
    variablesDataStructure = variablesDataStructure;
  }
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
        <div
          class="group_variable_div"
          id={`div_${item.id}`}
          draggable="true"
          on:dragstart={drag}
          on:dragover={allowDrop}
          on:drop={drop}
        >
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
