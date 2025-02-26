<script>
  export let label = "Picker";
  export let exploreGroupsOpen = false;

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
    >{label}
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
  <div id="select_var" class="select_var" class:exploreGroupsOpen>
    <slot />
  </div>
</fieldset>

<style>
  fieldset {
    border: none;
    display: inline;
    max-width: 60em;
  }
  fieldset.exploreGroupsOpen {
    border: 2px solid;
    padding-left: 30px;
    padding-right: 40px;
    padding-bottom: 50px;
    background-color: #eee;
    margin: 3em;
    display: block;
  }
  .exploreGroupsOpen svg {
    transform: translateY(6px) translateX(6px) rotate(0.25turn);
  }
  /*  Toggle open/close behavior.
    This div is not displayed by default.
    However, when the parent has the exploreGroupsOpen class,
    the display: block style overrides.
*/
  div#select_var {
    display: none;
  }
  div.exploreGroupsOpen#select_var {
    display: block;
  }
</style>
