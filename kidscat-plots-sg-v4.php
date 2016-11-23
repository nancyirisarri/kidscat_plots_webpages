<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Comparison ingested with created KiDS-CAT plots</title>
</head>

<body>
<h2><a href="http://home.strw.leidenuniv.nl/~irisarri/kidscat-plots-sg-v0.php">see plots using biweight scale, constant=9.0</a></h2>
<h2><a href="http://home.strw.leidenuniv.nl/~irisarri/kidscat-plots-sg-v1.php">see plots using biweight scale, constant=2.5/0.6745</a></h2>
<h2><a href="http://home.strw.leidenuniv.nl/~irisarri/kidscat-plots-sg-v2.php">see plots using fortran bwsm, without par(2)</a></h2>
<?php

  $dir = '/home/irisarri/public_html/kidscat_plots/';

  $obs = array_diff(scandir($dir), array('..', '.'));
  sort($obs);

  //print_r($contents);

  foreach($obs as $ob) {
    $dir = '/home/irisarri/public_html/kidscat_plots/';

    echo "<h1>{$ob}</h1>";

    //include "kidscat_plots/{$ob}/{$ob}.html";

    echo "<table width='100%'>
      <tr>
      <td></td>
      <td>SG</td>
      </tr>
      <tr>
      <td>original</td>";

    $images = array_diff(scandir($dir . $ob . "/from_awe"), array('..', '.'));

    sort($images);

    foreach($images as $image) {
      if (substr($image, -6) == "SG.png") {
        $location = "kidscat_plots/{$ob}/from_awe/{$image}";
        echo "<td><a href=\"{$location}\" target=\"_blank\"><img height=\"256\" width=\"256\" src=\"{$location}\"></a></td>";
      }
    }

    echo "</tr><tr><td>fortran bwsm, with par(2)</td>";

    $dir = '/home/irisarri/public_html/kidscat_plots_sg_v4/';

    $images = array_diff(scandir($dir . $ob), array('..', '.'));

    sort($images);

    foreach($images as $image) {
      $location = "kidscat_plots_sg_v4/{$ob}/{$image}";

      echo "<td><a href=\"{$location}\" target=\"_blank\"><img height=\"256\" width=\"256\" src=\"{$location}\"></a></td>";
    }

    echo "</tr><tr><td>ingested</td>";

    $dir = '/home/irisarri/public_html/kidscat_plots/';

    $images = array_diff(scandir($dir . $ob), array('..', '.'));

    sort($images);

    foreach($images as $image) {
      if (substr($image, -6) == "SG.png") {
        $location = "kidscat_plots/{$ob}/{$image}";

        echo "<td><a href=\"{$location}\" target=\"_blank\"><img height=\"256\" width=\"256\" src=\"{$location}\"></a></td>";
      }
    }

    echo "</tr></table><br>";
  }

?>

</body>
</html>
