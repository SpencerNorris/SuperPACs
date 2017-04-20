// d3-combined.js
import * as array from 'd3-array';
import * as color from 'd3-color';
import * as dispatch from 'd3-dispatch';
import * as drag from 'd3-drag';
import * as force from 'd3-force';
import * as path from 'd3-path';
import * as scale from 'd3-scale';
import * as selection from 'd3-selection';
import * as shape from 'd3-shape';
import * as transition from 'd3-transition';
import * as zoom from 'd3-zoom';
import {event}  from 'd3-selection';

export default Object.assign({getEvent: () => require("d3-selection").event,},
  array,
  color,
  dispatch,
  drag,
  force,
  path,
  scale,
  selection,
  shape,
  transition,
  zoom
);
