<script>
  import { tick } from "svelte";
  import { scaleLinear } from "d3-scale";
  import { line, curveBumpX } from "d3-shape";
  export let numbers;

  let colorNames = [
    "Crimson",
    "DeepPink",
    "Coral",
    "Magenta",
    "Chartreuse",
    "DarkOliveGreen",
    "PaleTurquoise",
    "RoyalBlue",
    "Sienna",
    "DarkSlateGray",
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

  function widthPointsForPop(pop) {
    if (pop.histogram) return 5;
    return 1;
  }

  function markup(population, minDim, maxDim, level) {
    population.minDim = minDim;
    population.maxDim = maxDim;
    population.yPlace = scaleLinear().domain([0, 1]).range([minDim, maxDim]);
    population.level = level;
    population.color = getNextColor();
      if (typeof population.data == "number") {
        population.xScale = scaleLinear().domain([0, population.total]).range([0, 1]);
	if (population.histogram) {
	   let peak = findDensityPeak(population.histogram);
	  population.histogramY = scaleLinear().domain([0, peak]).range([0.8, 0.05]);
	}
      } else {
        let widthPoints = 0;
        for (let i = 0; i < population.data.length; ++i) {
	  widthPoints += widthPointsForPop(population.data[i]);
	}
        let childWidth = (maxDim - minDim) / widthPoints;
	let pointsSoFar = 0;
        for (let i = 0; i < population.data.length; ++i) {
          markup(
            population.data[i],
            minDim + pointsSoFar * childWidth,
            minDim + (pointsSoFar + widthPointsForPop(population.data[i])) * childWidth,
            level + 1
          );
	  pointsSoFar += widthPointsForPop(population.data[i]);
        }
      }
    return population;
  }

  function hasAnyHistograms(population) {
    if (!population) return false;
    if (!population.data) return false;
    if (typeof population.data == "number") {
      if (population.histogram) return true;
    }
    else {
       for (let i = 0; i < population.data.length; ++i) {
          if (hasAnyHistograms(population.data[i])) return true;
       }
    }
    return false;
  }

  $: aData = markup(deepCopy(numbers), 0, 1, 0);

  $: hasHistograms = hasAnyHistograms(aData);

  $: maxTotal = findMaxTotal(aData);

  $: levels = findLevels(aData);

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
      if (typeof population.data != "number") {
        a = population.data.map((pop) => findPopulations(pop));
      }
      if (population.histogram) {
	let fraction = (widthPointsForPop(population)-1)/widthPointsForPop(population);
	let divide = (fraction*(population.maxDim-population.minDim)+population.minDim);
        let posBar = {...population, histogram:null, type:'counts', minDim:divide};
	let distribution = {...population, label:'distribution', color:getNextColor(), maxDim:divide};
	posBar.yPlace = scaleLinear().domain([0, 1]).range([posBar.minDim, posBar.maxDim]);
	distribution.yPlace = scaleLinear().domain([0, 1]).range([distribution.minDim, distribution.maxDim]);
	a.push(posBar);
	a.push(distribution);
      }
      else {
         a.push(population);
      }
    return a.flat(Infinity);
  }

  function populationsAtLevel(population, n) {
    return findPopulations(population).filter((pop) => pop.level == n);
  }

  function populationsWithGroupTotals(population) {
    return findPopulations(population).filter((pop) => pop.showTotal);
  }     

  function populationsWithDetail(population) {
    return findPopulations(population).filter((pop) => pop.isLeaf);
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
  $: longestLevel_5 = longestStringAtLevel(aData, 5);

  let strSizer_1;
  let strSizer_2;
  let strSizer_3;
  let strSizer_4;
  let strSizer_5;
  let strSizer_total;

  let bb_1, bb_2, bb_3, bb_4, bb_5,bb_total;
  let labelAreaWidth = 0;
  let total_nums_width = 0;

  function updateSizes() {
    tick().then(() => {
      bb_1 = strSizer_1?.getBBox();
      bb_2 = strSizer_2?.getBBox();
      bb_3 = strSizer_3?.getBBox();
      bb_4 = strSizer_4?.getBBox();
      bb_5 = strSizer_5?.getBBox();
      bb_total = strSizer_total?.getBBox();
      labelAreaWidth = getLabelAreaWidth(bb_1, bb_2, bb_3, bb_4, bb_5);
      total_nums_width = bb_total ? bb_total.width : 0;
    });
  }

  $: updateSizes(
    longestLevel_1,
    longestLevel_2,
    longestLevel_3,
    longestLevel_4,
    longestLevel_5,    
  );

  function getLabelAreaWidth(bb_1, bb_2, bb_3, bb_4, bb_5) {
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
    if (bb_5 !== undefined) {
      sum += bb_4.width;
    }
    return sum;
  }

  function findDensityPeak(histogram) {
    let peak = 0;
    for (let bin of histogram) {
      if (bin.count > peak) {
        peak = bin.count;
      }
    }
    return peak;
  }

  $: histogramX = scaleLinear()
    .domain([0, 10])
    .range([labelAreaWidth + total_nums_width, width]);

  $: histogramY = scaleLinear().domain([0, 15000]).range([0.8, 0.05]);

  $: barX = scaleLinear()
    .domain([0, 1])
    .range([labelAreaWidth + total_nums_width, width]);

  $: popY = scaleLinear().domain([0, 1]).range([0, height]);

  function labelX(pop) {
    if (!width) return 0;
    if (bb_4 === undefined) return 0;
    let total = 0; //-(bb_1.width);
    if (pop.level >= 5) {
      total += bb_5.width;
    }
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

  $: minHeight = 4*(findPopulations(aData).length + 2) + "vh";
</script>

<h3>
  {numbers.dx}
</h3>

<div
  class="sizer"
  bind:clientWidth={width}
  bind:clientHeight={height}
  width="80vw"
>
  {#if width && aData}
    <svg width="100%" height={minHeight} >
      <g>
        {#if height > 20}
          <text x={barX(0) - total_nums_width} y="0"> total n </text>
	  {#each populationsWithGroupTotals(aData) as pop}
            {#if pop.total}
              <text
                x={barX(0) - total_nums_width}
                y={popY(pop.yPlace(0.5)) + 5}
              >
                {pop.total.toLocaleString()}
              </text>
            {/if}
	  {/each}
          {#each populationsWithDetail(aData) as pop}
            {#if (pop.type == "counts")}
              <rect
                x={barX(0)}
                width={0.5 + barX(pop.xScale(pop.data)) - barX(0)}
                y={popY(pop.yPlace(0.05))}
                height={popY(pop.yPlace(0.95)) - popY(pop.yPlace(0.05))}
                fill={pop.color}
              />
              {#if (pop.ci_low !== undefined) && (pop.ci_high !== undefined) }
                <line
                  x1={barX(pop.xScale(pop.ci_low * pop.total))}
                  x2={barX(pop.xScale(pop.ci_high * pop.total))}
                  y1={popY(pop.yPlace(0.5))}
                  y2={popY(pop.yPlace(0.5))}
                  stroke="black"
                />
              {/if}
              {#if (pop.ci_low !== undefined)}
                <text
                  x={Math.max(
                    Math.min(
                      barX(pop.xScale(pop.data)) - 5,
                      barX(pop.xScale(pop.ci_low * pop.total)) - 2
                    ),
                    barX(0) + 50
                  )}
                  y={popY(pop.yPlace(0.5)) + 5}
                  text-anchor="end">{pop.data.toLocaleString()}</text
                >
              {/if}
            {:else if (pop.type == "histogram") && pop.histogram}
              <path
                d={line()
                  .curve(curveBumpX)
                  .x((d) => histogramX(d.viralLoadLog))
                  .y((d) => popY(pop.yPlace(pop.histogramY(d.count))))(
                  pop.histogram
                )}
                style={`stroke: ${pop.color}; fill: ${pop.color}`}
              />
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
              y1={popY(pop.yPlace(0.03))}
              y2={popY(pop.yPlace(0.97))}
              stroke="grey"
            />
            <line
              x1={labelX(pop, labelAreaWidth) + 4}
              x2={labelX(pop, labelAreaWidth) + 14}
              y1={popY(pop.yPlace(0.03))}
              y2={popY(pop.yPlace(0.03))}
              stroke="grey"
            />
            <line
              x1={labelX(pop, labelAreaWidth) + 4}
              x2={labelX(pop, labelAreaWidth) + 14}
              y1={popY(pop.yPlace(0.97))}
              y2={popY(pop.yPlace(0.97))}
              stroke="grey"
            />
          {/if}
        {/if}
        {#if pop.level > 0}
          <text
            x={labelX(pop, labelAreaWidth)}
            y={popY(pop.yPlace(0.5)) + 5}
            text-anchor="end"
          >
            {pop.label}
          </text>
        {/if}
      {/each}
      <g class="x-axis" transform={`translate(0, ${height+2})`} overflow="visible">
        <line x1={barX(0)} x2={barX(1)} y1="0" y2="0" stroke="black" />
        {#each [0.0, 0.2, 0.4, 0.6, 0.8, 1.0] as tick}
          <g class="tick" transform={`translate(${barX(tick)},0)`}>
            <foreignObject width="2.5em" height="2em" x="-0.5em" y="0.5em">
              <div class="exponentlabel">
                {Math.round(tick * 100)}%
              </div>
            </foreignObject>
            <line x1="0" x2="0" y1="0" y2="5" stroke="black" />
          </g>
        {/each}
      </g>
      {#if hasHistograms}
        <g class="x-axis" transform={`translate(0, -40)`}>
          <line x1={barX(0)} x2={barX(1)} y1="33" y2="33" stroke="black" />
          {#each [0, 3, 6, 9] as tick}
            <g class="tick" transform={`translate(${histogramX(tick)},0)`}>
              <foreignObject width="2em" height="2em" x="-0.5em" y="0.25em">
                <div class="exponentlabel">
                  10<sup>{tick}</sup>
                </div>
              </foreignObject>
              <line x1="0" x2="0" y1="33" y2="28" stroke="black" />
            </g>
          {/each}
        </g>
      {/if}

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
      <text x="-1000" y="-1000" bind:this={strSizer_5}
        >M {longestLevel_5}
      </text>
      <text x="-1000" y="-1000" bind:this={strSizer_total}>
        {#if maxTotal}
	        {maxTotal.toLocaleString()}
	{:else}
		0
	{/if}
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
