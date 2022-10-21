// for (int i = 1; i < histogram[channel].rows - 1; ++i)
//   smoothed_histogram[channel].at<float>(i) =
//       (histogram.at<float>(i - 1) + histogram.at<float>(i) +
//        histogram.at<float>(i + 1)) /3;