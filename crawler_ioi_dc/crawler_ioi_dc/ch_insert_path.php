
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>click demo</title>
    <style>
    p {
    color: red;
    margin: 5px;
    cursor: pointer;
    }
    p:hover {
    background: yellow;
    }
    </style>
    <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
</head>
<body>
 
<p>First Paragraph</p>
<p>Second Paragraph</p>
<p>Yet one more Paragraph</p>

<?php
echo("Hello");
//$conn = mysqli_connect('localhost', 'hurderella', 'chanbap61131', 'hurderella');
$conn = new mysqli('localhost', 'hurderella', 'chanbap61131', 'hurderella');
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$id = 0;
$url_file = fopen("chungha_db_500.txt", "r");
while(!feof($url_file)){
    $id++;
    $line = fgets($url_file);
    echo $line;

    $sql = "INSERT INTO url_list (url, id)
    VALUES ('".$line."', '".$id."')";

        if ($conn->query($sql) === TRUE) {
          echo "New record created successfully";
        } else {
          echo "Error: " . $sql . "<br>" . $conn->error;
        }
}
fclose($url_file);
$conn->close();
?>
<script>
$( "p" ).click(function() {
    $( this ).slideUp();
});
</script>
 
</body>
</html>