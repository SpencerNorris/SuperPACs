
function filter(obj, predicate) {
    let result = {};

    for (let key in obj) {
        if (obj.hasOwnProperty(key) && !predicate(obj[key])) {
            result[key] = obj[key];
        }
    }

    return result;
};

export default (filters, data) => {
    console.log(data)
    if(!filters.length) {
        return data;
    }



    return {committees: {}, donations: data.donations, representatives: {}};
}
