
function SeriesSliderArrows (
  seriescardsContainer,
  seriescontainerWidth,
  seriescardCount,
  seriescardWidth
) {
  if (
    $(seriescardsContainer).scrollLeft() + seriescontainerWidth <
    seriescardCount * seriescardWidth + 15
  ) {
    $("#series-slide-right").addClass("active");
  } else {
    $("#series-slide-right").removeClass("active");
  }
  if ($(seriescardsContainer).scrollLeft() > 0) {
    $("#series-slide-left").addClass("active");
  } else {
    $("#series-slide-left").removeClass("active");
  }
}
$(function() {
  // Scroll products' slider left/right
  let div = $("#series-cards-container");
  let seriescardCount = $(div)
    .find(".Series-Cards")
    .children(".Series-Card").length;
  let speed = 1000;
  let seriescontainerWidth = $(".SeriesCards").width();
  let seriescardWidth = 220;

  updateSeriesSliderArrowsStatus(div, seriescontainerWidth, seriescardCount, seriescardWidth);

  //Remove scrollbars
  $("#series-slide-right").click(function(e) {
    if ($(div).scrollLeft() + seriescontainerWidth < seriescardCount * seriescardWidth) {
      $(div).animate(
        {
          scrollLeft: $(div).scrollLeft() + seriescardWidth
        },
        {
          duration: speed,
          complete: function() {
            setTimeout(
              updateSliderArrowsStatus(
                div,
                seriescontainerWidth,
                seriescardCount,
                seriescardWidth
              ),
              1005
            );
          }
        }
      );
    }
    updateSeriesSliderArrowsStatus(div, seriescontainerWidth, seriescardCount, seriescardWidth);
  });
  $("#series-slide-left").click(function(e) {
    if ($(div).scrollLeft() + seriescontainerWidth > seriescontainerWidth) {
      $(div).animate(
        {
          scrollLeft: "-=" + seriescardWidth
        },
        {
          duration: speed,
          complete: function() {
            setTimeout(
              updateSeriesSliderArrowsStatus(
                div,
                seriescontainerWidth,
                seriescardCount,
                seriescardWidth
              ),
              1005
            );
          }
        }
      );
    }
    updateSeriesSliderArrowsStatus(div, seriescontainerWidth, seriescardCount, seriescardWidth);
  });

  // If resize action ocurred then update the container width value
  $(window).resize(function() {
    try {
      seriescontainerWidth = $("#series-cards-container").width();
      updateSeriesSliderArrowsStatus(div, seriescontainerWidth, seriescardCount, seriescardWidth);
    } catch (error) {
      console.log(
        `Error occured while trying to get updated slider container width: 
            ${error}`
      );
    }
  });
});



