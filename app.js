const port = process.env.PORT || 3000; // Use the PORT environment variable or default to 3000

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
