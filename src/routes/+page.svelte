<script>
  import { onMount } from "svelte";
  import * as util from "./util.js";
  import { URLforEndpoint } from "./fetching.js";
  import LabMenuBanner from "./LabMenuBanner.svelte";
  import BarGraph from "./BarGraph.svelte";
  import Histogram from "./Histogram.svelte";
  import VariablesPicker from "./VariablesPicker.svelte";

  let isLoading = true;
  let errorState = false;

  let dxList = null;
  let selectedDx = "Helicobacter pylori";
  let variablesDataStructure = null;
  let data = null;

  async function fetchDxList() {
    let url = URLforEndpoint("testlist")
    let response = await fetch(url);
    let items = await response.json();
    return Object.getOwnPropertyNames(items);
  }

  async function fetchVariables() {
     let url = URLforEndpoint("variables");
     let response = await fetch(url);
     let data = await response.json();
    loadVariableOptions(data);
  }

  async function loadOptions() {
    try {
      dxList = await fetchDxList();
      await fetchVariables();
      isLoading = false;
    } catch {
      errorState = true;
    }
  }

  onMount(async () => {
    loadOptions();
  });

  $: if (variablesDataStructure) {
    doQuery(variablesDataStructure, selectedDx);
  }

  function loadVariableOptions(data) {
    let options = data.items;
    for (let item of options) {
      Object.defineProperty(item, "checked", {
        get() {
          return this._checked;
        },
        set(newValue) {
          if (newValue == this._checked) return;
          for (let subItem of this.splits) {
            subItem._checked = newValue;
          }
          this._checked = newValue;
        },
      });
      let splits = item.splits;
      for (let subItem of splits) {
        subItem.owner = item;
        if (subItem._checked) {
          subItem.owner._checked = true;
        }
        Object.defineProperty(subItem, "checked", {
          get() {
            return this._checked;
          },
          set(newValue) {
            if (newValue == this._checked) return;
            this._checked = newValue;
            if (this._checked) {
              this.owner._checked = true;
            } else {
              let allOff = true;
              for (let subItem of this.owner.splits) {
                if (subItem._checked) {
                  allOff = false;
                  break;
                }
              }
              if (allOff) {
                this.owner._checked = false;
              }
            }
          },
        });
      }
    }
    variablesDataStructure = data;
  }

  async function doQuery(variablesDataStructure, dx) {
    isLoading = true;
    let url = URLforEndpoint("data");
    url += "/labbrowser";

    if (!variablesDataStructure) return;
      let params = {};
      for (let item of variablesDataStructure.items) {
        for (let subItem of item.splits) {
          if (subItem.checked) {
            if (!params.hasOwnProperty(item.id)) {
              params[item.id] = []
            }
            params[item.id].push(subItem.value);
          }
        }
      }

    let query_params = {
      "test_name": dx,
      "params": params,
    }
    console.log("request body: ", params);
    /* TODO: actually fetch data */
    console.log(url);
    let response = await fetch(url, {
      method:"POST",
      body:JSON.stringify(query_params),
       headers: {
       "Content-Type": "application/json",
       },   
      }) 
    data = await response.json();
    console.log(data);
    isLoading = false;
  }

  let numberFormatter = new Intl.NumberFormat("en-US", {
    maximumSignificantDigits: 4,
  });
</script>

<LabMenuBanner />

{#if !errorState}
  <div id="loading" class="hideLoading" class:isLoading>
    <img src="virus.gif" />
  </div>
{/if}
<header>
  <h1 class="page-top">Historic Results Browser</h1>

  <p class="body_text">
    Here we probably want some explanatory text...
    <span class="bold"> Please explore for yourself! </span>
  </p>
</header>

{#if errorState}
  <h1 class="errorText">
    <em
      ><strong>Sorry, an error occured. Please try re-loading the page.</strong
      ></em
    >
  </h1>
{:else}
  {#if dxList}
    <select name="dx" id="dx"
      bind:value={selectedDx}
    >
      {#each dxList as dx}
        <option value={dx} >{dx} </option>
      {/each}
    </select>
  {/if}

  <VariablesPicker bind:variablesDataStructure />

  {#if data}
    <div class="bar" >
      <BarGraph numbers={data} />
    </div>
  {/if}
{/if}

<footer>
  Any footer text here
  <p class="body_text">
    We appreciate your feedback. Please email us at
    <a class="email" href="mailto:rarnaout@bidmc.harvard.edu"
      >rarnaout@bidmc.harvard.edu</a
    >.
  </p>
</footer>

<style>
  .errorText {
    color: red;
    margin: auto;
    border: 3px solid red;
    border-radius: 4em;
    max-width: 16em;
  }

  .page-top {
    padding-top: 120px;
  }
  .print-page-top {
    padding-top: 0.5em;
    break-before: page;
  }
  @media only print {
    .print-page-top {
      padding-top: 120px;
    }
  }
  @media only print {
    .savebuttons {
      display: none;
    }
  }

  select#dx {
    margin: 20px auto;
    display: block;
  }

  /* Needs the :global directive to penetrate into @html strings: */
  :global(sup.exponent) {
    vertical-align: baseline;
    position: relative;
    top: -0.4em;
  }

  .histogram {
    width: 100%;
  }
  .all_groups {
    grid-area: max80emLeftContent;
    min-height: 500px;
    max-height: 800px;
  }
  .one_group {
    grid-area: max80emLeftContent;
    aspect-ratio: 1.618 / 1;
  }
  @media only print {
    .histogram {
      page-break-after: always;
    }
  }
  .groupcomment {
    font-size: 18px;
    line-height: 1.2em;
    padding-bottom: 0.7em;
  }
  .groupCommentSpace {
    padding-bottom: 1.5em;
  }
  @media only screen and (max-width: 72em) {
    .groupcomment {
      font-size: 14px;
      padding-bottom: 0.3em;
    }
  }

  div.bar {
     max-width: 900px;
     margin: auto;
  }

  .performance_commentary {
    margin-left: 10px;
  }

  .hideLoading {
    display: none;
  }
  .isLoading {
    display: block;
  }

  .showingBlock {
    display: block;
  }

  .showingAntigenPerformance {
    display: grid;
  }
  .anti_legend {
    padding-top: 1em;
  }

  .spacer {
    padding-top: 2em;
  }

  .legend {
    display: grid;
    grid-template-columns: 1.75em 1fr;
    grid-template-areas: "legendmark legendtext";
  }
  .legendmark {
    grid-area: legendmark;
    padding: 0.25em;
  }
  .legendtext {
    grid-area: legendtext;
  }
  .senspec_value {
    font-weight: 600;
  }
  .cm {
    padding-bottom: 0.5em;
  }
</style>
