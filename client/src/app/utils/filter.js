//Filtering utilities
//functionality realted to filtering data on the client side is placed here

//an enum defining all tha actions a filtering predicate can take on a object
const actions = Object.freeze({ADD: "1", DELETE: "2", PASS: "3"});

//an enum defining what type of object is getting filtered
const type = Object.freeze({GENERAL: "General",
                    REPRESENTATIVE: "Representative",
                    COMMITTEE: "Committee",
                    BILL: "Bill"});

/**
 * Filters the properties of the object based on the predicate function
 *
 * The object for every property is passed into the predicate
 * and the result of the predicate determines whether the property is kept of not
 * If the predicate returns true then the property is kept and vice versa
 *
 * Returns a new object with only accepted properties
 **/
function filterObject(obj, predicate) {
    let result = {};

    for (let key in obj) {
        if (obj.hasOwnProperty(key) && predicate(obj[key])) {
            result[key] = obj[key];
        }
    }

    return result;
};

/**
 * Filters the given data with the given filters
 *
 * The filters parameter is assumed to be an array of objects
 * which have predicate functions that return actions as defined above.
 * Data is kept in the data object if a predicate dictates an ADD action.
 * A predicate dictating a DELETE action will cause the object to be
 * removed from the data object.
 * A predicate dictating PASS will not affect the object.
 * An object which is entierly passed on will not be kept.
 * Earlier filters get higher priority than later ones.
 * The given data object is assumed to be graph data from the api.
 * An empty filters list causes no data to be kept.
 *
 * Returns a new object with the data elements dictated to be kept
 **/
function filter(filters, data) {
    //the predicate that processes each object by running all the predicates in filters
    let predicate = (type) => { return (obj) => {
        //loop through all the filters
        for(let f of filters) {
            //process this filter
            let r = f.predicate(obj, type);
            //if it doesn't pass, use the result to add/delete the object
            if(r != actions.PASS) {
                return r == actions.ADD;
            }
        }
        //default actions is to delete
        return false;
    };};

    //return the filtered data, donations are ignored because the graph
    //only chooses the needed ones
    return {committees: filterObject(data.committees, predicate(type.COMMITTEE)),
        donations: data.donations,
        representatives: filterObject(data.representatives, predicate(type.REPRESENTATIVE)),
        votes: data.votes,
        bills: filterObject(data.bills, predicate(type.BILL))};
}

//some general filters
let general = [
    {name: "Democrats", predicateFactory: (additive) => {
        return (obj, type) => {
            return obj.party === "D" ? (additive ? actions.ADD : actions.DELETE) : actions.PASS
        }}},
    {name: "Republicans", predicateFactory: (additive) => {
        return (obj, type) => {
            return obj.party === "R" ? (additive ? actions.ADD : actions.DELETE) : actions.PASS
        }}},
    {name: "Independents", predicateFactory: (additive) => {
        return (obj, type) => {
            return obj.party === "I" ? (additive ? actions.ADD : actions.DELETE) : actions.PASS
        }}}
];

//filter for a specific node, filters by name and type
let nodeFilterFactory = (item) => {
    return (additive) => {
        return (obj, type) => {
            if(item.type == type) {
                return obj.name == item.name ?
                    (additive ? actions.ADD : actions.DELETE) : actions.PASS;
            }
            return actions.PASS;
        };
    };
};

//filters for multiple nodes, filters by name and type
let multiNodeFilterFactory = (names, o_type) => {
    return (additive) => {
        return (obj, type) => {
            if(o_type == type) {
                for(let name of names) {
                    if(obj.name == name) {
                        return additive ? actions.ADD : actions.DELETE;
                    }
                }
            }
            return actions.PASS;
        };
    };
};

//export
export default {filter, actions, type, general, nodeFilterFactory, multiNodeFilterFactory};
