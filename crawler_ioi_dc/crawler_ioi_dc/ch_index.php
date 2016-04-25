
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
echo("Hello<br>\n");
//$conn = mysqli_connect('localhost', 'hurderella', 'chanbap61131', 'hurderella');
$conn = new mysqli('localhost', 'hurderella', 'chanbap61131', 'hurderella');
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT * FROM url_list";
$url_arr = array();
$result = $conn->query($sql);
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()){
        $row_url = rtrim($row["url"]); 
        array_push($url_arr, $row_url);
    }
} else {
    echo "Error: " . $sql . "<br>\n" . $conn->error;
}

#foreach ($url_arr as $key => $value) {
    # code...
#    echo $value;
#}
#http://dcimg2.dcinside.com/viewimage.php?id=3dafdf21f7d335ab67b1d1&no=29bcc427b38477a16fb3dab004c86b6fd0548bb7fdb4d15f49496390cca9d3ae48041c5607194ea75ff2242468f8938584db5b08ebef417ceab386719c
echo "<img src=\"http://dcimg2.dcinside.com/viewimage.php?id=3dafdf21f7d335ab67b1d1&no=29bcc427b38477a16fb3dab004c86b6fd0548bb7fdb4d15f49496390cca9d3ae48041c5607194ea75ff2242468f8938584db5b08ebef417ceab386719c\"/>";
#echo "<img src=\"".$url_arr[0]."\">";



$conn->close();
?>
<script>
$( "p" ).click(function() {
    $( this ).slideUp();
});
</script>
 <img src="http://dcimg2.dcinside.com/viewimage.php?id=3dafdf21f7d335ab67b1d1&no=29bcc427b38477a16fb3dab004c86b6fd0548bb7fdb4d15f49496390cca9d3ae48041c5607194ea75ff2242468f8938584db5b08ebef417ceab386719c" class="txc-image" style="clear:none;float:none;" />
</body>
</html>