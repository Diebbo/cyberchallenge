<?php
if(isset($_GET['url']) && !is_array($_GET['url'])){
$url = $_GET['url'];
$ch = curl_init($url);
    curl_setopt ($ch, CURLOPT_FOLLOWLOCATION, 0);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    echo curl_exec($ch);
    curl_close($ch);
return;
}

?>
<html>
<head>
    <meta charset="utf-8">
    <title>SSRF Example</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.4/css/bulma.min.css">
</head>
<body>
<section class="hero">
  <div class="hero-body">
    <div class="container">
      <h1 class="title">
        Basic SSRF
      </h1>
      <h2 class="subtitle">
        Yeah, this may seems hard. As always the flag is in get_flag.php. The source code <a href="/?source">here</a>
      </h2>
    </div>
  </div>
</section>
    <section class="section">
        <div class="container">
    
        <form method="GET">
            <div class="field">
                <div class="control">
                    <input class="input" type="text" placeholder="Try url" name="url">
                </div>
            </div>
            <div class="field">
                <div class="control">
                    <input class="submit" type="submit" placeholder="Send" value="Send">
                </div>
            </div>      
        </form>
        </div>
    </section>
</body>
</html>
