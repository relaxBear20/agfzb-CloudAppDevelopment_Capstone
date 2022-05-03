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
         let dl = await cloudant.use("dealerships").list({include_docs:true}).rows.forEach(element => {
            let temp = {}
            
         });
         return { "data": dl };
     } catch (error) {
         return { error: error.description };
     }
 
 }