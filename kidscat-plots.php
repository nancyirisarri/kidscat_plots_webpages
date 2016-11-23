<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Comparison ingested with created KiDS-CAT plots</title>
</head>

<body>

<?php

  $dir = '/home/irisarri/public_html/kidscat_plots/';

  $obs = array_diff(scandir($dir), array('..', '.'));
  sort($obs);

  foreach($obs as $ob) {
    echo "<h1>{$ob}</h1>";

    include "kidscat_plots/{$ob}/{$ob}.html";

    echo "<table width='100%'>
      <tr>
      <td></td>
      <td>ABMAGSAT</td>
      <td>COMPL</td>
      <td>FWHMSN</td>
      <td>MLIM</td>
      <td>SG</td>
      </tr>
      <tr>
      <td>ingested</td>";

    $images = array_diff(scandir($dir . $ob), array('..', '.', 'from_awe'));

    sort($images);

    foreach($images as $image) {
      if (substr($image, -3) == "png" and substr($image, 0, 4) == "KiDS") {
        $location = "kidscat_plots/{$ob}/{$image}";

        echo "<td><a href=\"{$location}\" target=\"_blank\"><img height=\"256\" width=\"256\" src=\"{$location}\"></a></td>";
      }
    }

    echo "</tr><tr><td>from AWE</td>";

    $images_awe = array_diff(scandir($dir . $ob . "/from_awe"), array('..', '.'));

    sort($images_awe);

    foreach($images_awe as $image) {
      $location = "kidscat_plots/{$ob}/from_awe/{$image}";

      echo "<td><a href=\"{$location}\" target=\"_blank\"><img height=\"256\" width=\"256\" src=\"{$location}\"></a></td>";
    }

    echo "</tr></table><br>";
  }

?>

</body>
</html>
