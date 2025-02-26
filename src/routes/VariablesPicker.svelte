<script>
  export let variablesDataStructure;

  function resetChecks() {
    for (let item of variablesDataStructure.items) {
      item.checked = false;
    }
    variablesDataStructure = variablesDataStructure;
  }

  let exploreGroupsOpen = false;
  function toggleGroupsOpen() {
    exploreGroupsOpen = !exploreGroupsOpen;
  }

  function isDescendentOf(widget, tag, className) {
    while (widget) {
      if (widget.tagName == tag) {
        if (widget.classList.contains(className)) {
          return true;
        }
      }
      widget = widget.parentNode;
    }
    return false;
  }

  function closeExploreGroups(event) {
    if (isDescendentOf(event.target, "DIV", "select_var")) return;
    if (isDescendentOf(event.target, "FIELDSET", "exploreGroupsOpen")) return;
    exploreGroupsOpen = false;
  }
</script>

<fieldset class:exploreGroupsOpen>
  <legend
    id="select_var_label"
    class="select_var_label"
    on:click={toggleGroupsOpen}
    >Explore groups
    <svg height="20px" width="20px" overflow="visible">
      <g transform="translate(4,8)">
        <line
          x1="0"
          y1="0"
          x2="6"
          y2="6"
          stroke="black"
          stroke-width="3"
          stroke-linecap="round"
        />
        <line
          x1="6"
          y1="6"
          x2="0"
          y2="12"
          stroke="black"
          stroke-width="3"
          stroke-linecap="round"
        />
      </g>
    </svg>
  </legend>
  <div id="select_var" class="select_var">
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
</fieldset>

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

  /*  Toggle open/close behavior.
    This div is not displayed by default.
    However, when the parent has the exploreGroupsOpen class,
    the display: block style overrides.
*/
  div#select_var {
    display: none;
  }
  .exploreGroupsOpen > div#select_var {
    display: block;
  }

  fieldset {
    border: none;
    display: inline;
  }
  fieldset.exploreGroupsOpen {
    border: 2px solid;
    padding-left: 30px;
    padding-right: 40px;
    padding-bottom: 50px;
    background-color: #eee;
    margin: 0px 7em;
    display: block;
  }
  .exploreGroupsOpen svg {
    transform: translateY(6px) translateX(6px) rotate(0.25turn);
  }
</style>
