<script>
  export let label = "Picker";
  export let exploreGroupsOpen = false;

  function toggleGroupsOpen() {
    exploreGroupsOpen = !exploreGroupsOpen;
  }

  function clicky() {
    exploreGroupsOpen = false;  
  }
</script>

<fieldset class:exploreGroupsOpen>
  <legend
    id="select_var_label"
    class="select_var_label"
    on:click={toggleGroupsOpen}
    >{label}
    <svg height="20px" width="20px" overflow="visible" class="toggle">
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
  {#if exploreGroupsOpen}
  <div class="closeButton" ><button on:click={clicky}>
    <svg width=30 height=30 overflow="visible" >
      <line x1="0" x2="30" y1="0" y2="30" stroke="black" stroke-width="2"/>
      <line x1="0" x2="30" y1="30" y2="0" stroke="black" stroke-width="2"/>
      <line x1="0" x2="0" y1="30" y2="0" stroke="black" stroke-width="2"/>
      <line x1="30" x2="30" y1="30" y2="0" stroke="black" stroke-width="2"/>
      <line x1="0" x2="30" y1="0" y2="0" stroke="black" stroke-width="2"/>
      <line x1="0" x2="30" y1="30" y2="30" stroke="black" stroke-width="2"/>
    </svg>
  </button></div>
  {/if}
  <div id="select_var" class="select_var" class:exploreGroupsOpen>
    <slot />
  </div>
</fieldset>

<style>
  .closeButton {
    margin: 0px;
    padding: 0px;
    border: none;
    position: sticky;
    top: 60px;
    width:max-content;
    margin-left:auto;
  }
  button {
    border: none;
  }
  fieldset {
    border: none;
    display: inline;
    max-width: 60em;
  }
  fieldset.exploreGroupsOpen {
    border: 2px solid;
    padding-top: 0px;
    padding-left: 30px;
    padding-right: 30px;
    padding-bottom: 30px;
    background-color: #eee;
    margin: 3em;
    display: block;
  }
  .exploreGroupsOpen .toggle {
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
