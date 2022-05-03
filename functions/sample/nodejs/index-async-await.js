/**
 * Get all dealerships
 */

const Cloudant = require('@cloudant/cloudant');


async function main(params) {
    const cloudant = Cloudant({
        url: "https://28612cb3-162b-4c6e-a985-8fb6a22cc102-bluemix.cloudantnosqldb.appdomain.cloud",
        plugins: { iamauth: { iamApiKey: "wvkVgyelZMIoco-hqDkt1S9yRIWYBg-Y63IagQv_291G" } }
    });


    try {
        var dl1 = []
        let dl = await cloudant.use("dealerships").list({ include_docs: true })
        const docs = dl.rows.map((r) => {
            return {
                "address": r.doc.address,
                "city": r.doc.city,
                "full_name": r.doc.full_name,
                "id": r.doc.id,
                "lat": r.doc.lat,
                "long": r.doc.long,
                "short_name": r.doc.short_name,
                "st": r.doc.st,
                "state": r.doc.state,
                "zip": r.doc.zip,

            }
        }).filter(a => {
            var p = params.state == null ? "" : params.state.toLowerCase();
            return a.st.toLowerCase().indexOf(p) >= 0
        })
        return { "data": docs }
        return docs;
    } catch (error) {
        return { error: error.description };
    }

}