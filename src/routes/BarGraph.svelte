<script>
  import { tick } from "svelte";
  import { scaleLinear } from "d3-scale";
  export let numbers;

  let colorNames = [
    "Crimson",
    "DeepPink",
    "Coral",
    "PaleGoldenrod",
    "Magenta",
    "Chartreuse",
    "DarkOliveGreen",
    "PaleTurquoise",
    "RoyalBlue",
    "BlanchedAlmond",
    "Sienna",
    "DarkSlateGray",
    "AliceBlue",
    "Chocolate",
    "DarkBlue",
    "DarkGreen",
    "DarkSalmon",
    "DarkViolet",
    "ForestGreen",
    "Fuchsia",
    "Gold",
  ];
  let colorIterator = 0;

  function getNextColor() {
    let a = colorNames[colorIterator];
    colorIterator += 1;
    colorIterator = colorIterator % colorNames.length;
    return a;
  }

  let width;
  let height;

  function deepCopy(x) {
    let s = JSON.stringify(x);
    let theCopy = JSON.parse(s);
    return theCopy;
  }

  function markup(population, minDim, maxDim, level) {
    population.minDim = minDim;
    population.maxDim = maxDim;
    population.level = level;
    population.color = getNextColor();
    if (population.data) {
      if (typeof population.data != "number") {
        let childWidth = (maxDim - minDim) / population.data.length;
        for (let i = 0; i < population.data.length; ++i) {
          markup(
            population.data[i],
            minDim + i * childWidth,
            minDim + (i + 1) * childWidth,
            level + 1
          );
        }
      }
    }
    return population;
  }

  $: aData = markup(deepCopy(numbers), 0, 1, 0);

  $: maxValue = findMaxValue(aData);
  $: maxTotal = findMaxTotal(aData);

  $: levels = findLevels(aData);

  function findMaxValue(population) {
    if (typeof population.data == "number") {
      return population.data;
    }
    let maxVal = 0.0;
    if (population.data) {
      for (let i = 0; i < population.data.length; ++i) {
        let val = findMaxValue(population.data[i]);
        if (val > maxVal) {
          maxVal = val;
        }
      }
    }
    return maxVal;
  }

  function findMaxTotal(population) {
    if (typeof population.data == "number") {
      if (population.total) {
        return population.total;
      }
    } else if (Array.isArray(population.data)) {
      let maxVal = 0.0;
      if (population.data) {
        for (let i = 0; i < population.data.length; ++i) {
          let val = findMaxTotal(population.data[i]);
          if (val > maxVal) {
            maxVal = val;
          }
        }
      }
      return maxVal;
    } 
  }

  function findLevels(population) {
    if (!population) return 0;
    if (typeof population.data == "number") return 0;
    let maxDepth = 0;
    if (population.data) {
      for (let i = 0; i < population.data.length; ++i) {
        let childDepth = findLevels(population.data[i]);
        if (childDepth > maxDepth) maxDepth = childDepth;
      }
    }
    return maxDepth + 1;
  }

  function findPopulations(population) {
    let a = [];
    if (!population) return a;
    if (population.data) {
      if (typeof population.data != "number") {
        a = population.data.map((pop) => findPopulations(pop));
      }
      a.push(population);
    }
    return a.flat();
  }

  function populationsAtLevel(population, n) {
    return findPopulations(population).filter((pop) => pop.level == n);
  }

  function longestStringAtLevel(population, n) {
    let winner = "";
    let pops = populationsAtLevel(population, n);
    for (let i = 0; i < pops.length; ++i) {
      if (pops[i].label.length > winner.length) {
        winner = pops[i].label;
      }
    }
    return winner;
  }

  $: longestLevel_1 = longestStringAtLevel(aData, 1);
  $: longestLevel_2 = longestStringAtLevel(aData, 2);
  $: longestLevel_3 = longestStringAtLevel(aData, 3);
  $: longestLevel_4 = longestStringAtLevel(aData, 4);

  let strSizer_1;
  let strSizer_2;
  let strSizer_3;
  let strSizer_4;
  let strSizer_total;

  let bb_1, bb_2, bb_3, bb_4, bb_total;
  let labelAreaWidth = 0;
  let total_nums_width = 0;

  function updateSizes() {
    tick().then(() => {
      bb_1 = strSizer_1?.getBBox();
      bb_2 = strSizer_2?.getBBox();
      bb_3 = strSizer_3?.getBBox();
      bb_4 = strSizer_4?.getBBox();
      bb_total = strSizer_total?.getBBox();
      labelAreaWidth = getLabelAreaWidth(bb_1, bb_2, bb_3, bb_4);
      total_nums_width = bb_total ? bb_total.width : 0;
    });
  }

  $: updateSizes(
    longestLevel_1,
    longestLevel_2,
    longestLevel_3,
    longestLevel_4
  );

  function getLabelAreaWidth(bb_1, bb_2, bb_3, bb_4) {
    let sum = 0;
    if (bb_1 !== undefined) {
      sum += bb_1.width;
    }
    if (bb_2 !== undefined) {
      sum += bb_2.width;
    }
    if (bb_3 !== undefined) {
      sum += bb_3.width;
    }
    if (bb_4 !== undefined) {
      sum += bb_4.width;
    }
    return sum;
  }

  function ciLow(pop) {
    let p = pop.ci_low;
    let prop = p * (pop.total / maxValue);
    let x = (width - (labelAreaWidth + total_nums_width)) * prop;
    return barX(pop) + x;
  }

  function ciHigh(pop) {
    let p = pop.ci_high;
    let prop = pop.ci_high * (pop.total / maxValue);
    let x = (width - (labelAreaWidth + total_nums_width)) * prop;
    return barX(pop) + x;
  }

  $: histogramX = scaleLinear()
    .domain([0, 10])
    .range([labelAreaWidth + total_nums_width, width]);

  function barX(pop) {
    return labelAreaWidth + total_nums_width;
  }

  function barNumberX(pop) {
    let x = barX(pop) + barWidth(pop) - 5;
    if (x > ciLow(pop) - 2) {
      x = ciLow(pop) - 2;
    }
    if (x < barX(pop) + 50) {
      // TODO: make this more precise
      x = ciHigh(pop) + 54;
    }
    return x;
  }

  function barWidth(pop) {
    return (
      (width - (labelAreaWidth + total_nums_width)) * (pop.data / maxValue)
    );
  }

  $: popY = scaleLinear().domain([0, 1]).range([0, height]);

  function barY(pop) {
    return popY(pop.minDim + 0.05 * (pop.maxDim - pop.minDim));
  }

  function barHeight(pop) {
    return height * 0.9 * (pop.maxDim - pop.minDim);
  }

  function labelX(pop) {
    if (!width) return 0;
    if (bb_4 === undefined) return 0;
    let total = 0; //-(bb_1.width);
    if (pop.level >= 4) {
      total += bb_4.width;
    }
    if (pop.level >= 3) {
      total += bb_3.width;
    }
    if (pop.level >= 2) {
      total += bb_2.width;
    }
    if (pop.level >= 1) {
      total += bb_1.width;
    }

    return total;
  }

  function labelY(pop) {
    return height * pop.minDim + 0.5 * height * (pop.maxDim - pop.minDim);
  }
</script>

<h3>
  {numbers.dx}
</h3>

<div
  class="sizer"
  bind:clientWidth={width}
  bind:clientHeight={height}
  height="60vh"
  width="80vw"
>
  {#if width && numbers}
    <svg width="100%" height="60vh">
      <g>
        {#if height > 20}
          <text x={barX(labelAreaWidth) - total_nums_width} y="0">
            total n
          </text>
          {#each populationsAtLevel(aData, levels) as pop}
            {#if pop.type == "counts"}
              <rect
                x={barX(pop, labelAreaWidth)}
                width={barWidth(pop, labelAreaWidth)}
                y={barY(pop)}
                height={barHeight(pop)}
                fill={pop.color}
              />
              {#if pop.ci_low && pop.ci_high}
                <line
                  x1={ciLow(pop, labelAreaWidth)}
                  x2={ciHigh(pop, labelAreaWidth)}
                  y1={barY(pop) + 0.5 * barHeight(pop)}
                  y2={barY(pop) + 0.5 * barHeight(pop)}
                  stroke="black"
                />
              {/if}
              {#if pop.data > 0 && pop.ci_low !== undefined}
                <text
                  x={barNumberX(pop, labelAreaWidth)}
                  y={barY(pop) + barHeight(pop) / 2 + 5}
                  text-anchor="end">{pop.data.toLocaleString()}</text
                >
              {/if}
            {:else if pop.type == "histogram"}
              {#each pop.histogram as bar}
                <line
                  x1={histogramX(bar["viralLoadLog"])}
                  x2={histogramX(bar["viralLoadLog"])}
                  y1={popY(pop.maxDim)}
                  y2={popY(pop.maxDim) - 0.004 * bar["count"]}
                  stroke={pop.color}
                  stroke-width="4"
                />
              {/each}
            {/if}
            {#if pop.total}
              <text
                x={barX(pop, labelAreaWidth) - total_nums_width}
                y={barY(pop) + barHeight(pop) / 2 + 5}
              >
                {pop.total.toLocaleString()}
              </text>
            {/if}
          {/each}
        {/if}
      </g>
      {#each findPopulations(aData) as pop}
        {#if pop.level < levels}
          {#if pop.level > 0}}
            <line
              x1={labelX(pop, labelAreaWidth) + 4}
              x2={labelX(pop, labelAreaWidth) + 4}
              y1={height * pop.minDim + 14}
              y2={height * pop.maxDim - 24}
              stroke="black"
            />
            <line
              x1={labelX(pop, labelAreaWidth) + 4}
              x2={labelX(pop, labelAreaWidth) + 14}
              y1={height * pop.minDim + 14}
              y2={height * pop.minDim + 14}
              stroke="black"
            />
            <line
              x1={labelX(pop, labelAreaWidth) + 4}
              x2={labelX(pop, labelAreaWidth) + 14}
              y1={height * pop.maxDim - 24}
              y2={height * pop.maxDim - 24}
              stroke="black"
            />
          {/if}
        {/if}
        {#if pop.level > 0}
          <text
            x={labelX(pop, labelAreaWidth)}
            y={labelY(pop, height, labelAreaWidth)}
            text-anchor="end"
          >
            {pop.label}
          </text>
        {/if}
      {/each}

      <!-- Discreetly find out the text size of our labels -->
      <text x="-1000" y="-1000" bind:this={strSizer_1}
        >M {longestLevel_1}
      </text>
      <text x="-1000" y="-1000" bind:this={strSizer_2}
        >M {longestLevel_2}
      </text>
      <text x="-1000" y="-1000" bind:this={strSizer_3}
        >M {longestLevel_3}
      </text>
      <text x="-1000" y="-1000" bind:this={strSizer_4}
        >M {longestLevel_4}
      </text>
      <text x="-1000" y="-1000" bind:this={strSizer_total}>
        {maxTotal.toLocaleString()}
      </text>
    </svg>
  {/if}
</div>

<style>
  div.sizer {
    margin-top: 20px;
    margin-right: 100px;
    margin-bottom: 20px;
    margin-left: 100px;
  }
  h3 {
    margin: auto;
    text-align: center;
  }
  svg {
    /* Note that both of these must be set to keep the graphic from going over the
      top menu banner: */
    position: relative;
    z-index: -1;
    overflow: visible;
  }
</style>
