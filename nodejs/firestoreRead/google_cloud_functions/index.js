// https://cloud.google.com/firestore/docs/create-database-server-client-library?hl=ja#node.js_1
// https://cloud.google.com/functions/docs/tutorials/use-cloud-bigtable?hl=ja

const functions = require('@google-cloud/functions-framework');
const Firestore = require('@google-cloud/firestore');

// if (!process.env.PROJECT)
//   console.log('env PROJECT is not set.');
//   process.exit();
// const project = process.env.PROJECT;

const db = new Firestore({
  projectId: process.env.GCP_PROJECT,
});

exports.firestoreRead = async (req, res) => {
  const snapshot = await db.collection('users').get();
  snapshot.forEach((doc) => {
    console.log(doc.id, '=>', doc.data());
  });
  res.status(200).end();
};