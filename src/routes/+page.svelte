<script>
  import { onMount } from "svelte";
  import * as util from "./util.js";
  import { URLforEndpoint } from "./fetching.js";
  import LabMenuBanner from "./LabMenuBanner.svelte";
  import BarGraph from "./BarGraph.svelte";
  import VariablesPicker from "./VariablesPicker.svelte";

  let isLoading = true;
  let errorState = false;

  let dxList = null;
  let selectedDx = "Helicobacter pylori";
  let variablesDataStructure = null;
  let data = null;

  async function fetchDxList() {
    let url = URLforEndpoint("testlist");
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

    if (!variablesDataStructure) return;

    // Identify which variables have any levels checked
    let parameter_variables = [];
    for (let item of variablesDataStructure.items) {
      for (let subItem of item.splits) {
        if (subItem.checked) {
          parameter_variables.push(item);
          break;
        }
      }
    }

    let params = {};
    for (let item of parameter_variables) {
      params[item.id] = [];
    }

    for (let item of parameter_variables) {
      for (let subItem of item.splits) {
        if (subItem.checked) {
          params[item.id].push(subItem.value);
        }
      }
    }

    let url = URLforEndpoint("data") + "/labbrowser";
    let query_params = {
      test_name: dx,
      params: params,
    };
    /* actually fetch data */
    let response = await fetch(url, {
      method: "POST",
      body: JSON.stringify(query_params),
      headers: {
        "Content-Type": "application/json",
      },
    });
    data = await response.json();
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
  <div class="pickers">
    {#if dxList}
      <select name="dx" id="dx" bind:value={selectedDx}>
        {#each dxList as dx}
          <option value={dx}>{dx} </option>
        {/each}
      </select>
    {/if}

    <VariablesPicker bind:variablesDataStructure />
  </div>

  <div class="bar">
    {#if data}
      <BarGraph numbers={data} />
    {/if}
  </div>
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

  div.pickers {
    margin: auto;
    display: flex;
    flex-wrap: wrap;
    flex-direction: row; /* default */
    justify-content: center;
    align-items: center; /* center items vertically */
  }

  div.bar {
    margin: 4em 0px;
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
  @media only print {
    .histogram {
      page-break-after: always;
    }
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

  .spacer {
    padding-top: 2em;
  }
</style>
