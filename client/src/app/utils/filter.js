//Filtering utilities
//functionality realted to filtering data on the client side is placed here

//an enum defining all tha actions a filtering predicate can take on a object
const actions = Object.freeze({ADD: "1", DELETE: "2", PASS: "3"});

//an enum defining what type of object is getting filtered
const type = Object.freeze({GENERAL: "General",
                    REPRESENTATIVE: "Representative",
                    COMMITTEE: "Committee"});

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
        representatives: filterObject(data.representatives, predicate(type.REPRESENTATIVE))};
}

//some general filters
let general = [{name: "Democrats", predicate: (obj, type) => {return obj.party === "D" ? actions.ADD : actions.PASS}},
    {name: "Republicans", predicate: (obj, type) => {return obj.party === "R" ? actions.ADD : actions.PASS}},
    {name: "Independents", predicate: (obj, type) => {return obj.party === "I" ? actions.ADD : actions.PASS}}];

//export
export default {filter, actions, type, general};
