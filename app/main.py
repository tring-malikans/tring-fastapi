import uvicorn

if __name__ == '__main__':
    uvicorn.run('server.app:app', host="0.0.0.0", port=9000, reload=True)




#     const doc = collection.find().toArray().then(items=>{
#     console.log(`Successfully found ${items.length} documents.`);
#     items.forEach(i=>{
#       console.log(Object.values(i));
#     });
#   });


#   const doc1 = collection.findOne({}, { sort: { '_id':-1 }}).then(result=>{
#     if(result) {
#       console.log(`Successfully found document: ${result}.`);
#       console.log(Object.keys(result))
#       return result
#     } else {
#       console.log("No document matches the provided query.");
#     }
#   });
#   const


#   const doc2=collection.aggregate(
#    [
#      { $sort : { '_id' : -1 } }
#    ]
#   ).toArray().then(items=>{
#     console.log(items,'f')
#   })
# console.log(Object.keys(doc2))