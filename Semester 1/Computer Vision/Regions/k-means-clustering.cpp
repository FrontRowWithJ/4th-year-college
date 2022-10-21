// // Store the image pixels as an array of samples
// Mat samples(image.rows *image.cols, 3, CV_32F);
// float *sample = samples.ptr<float>(0);
// for (int row = 0; row < image.rows; row++)
//   for (int col = 0; col < image.cols; col++)
//     for (int channel = 0; channel < 3; channel++)
//       samples.at<float>(row *image.cols + col, channel) =
//           (uchar)image.at<Vec3b>(row, col)[channel];
// // Apply k-means clustering, determining the cluster
// // centres and a label for each pixel.

// Mat labels, centres;
// kmeans(samples, k, labels, TermCriteria(CV_TERMCRIT_ITER | CV_TERMCRIT_EPS, 0.0001, 10000), iterations,
//        KMEANS_PP_CENTERS, centres);
// // Use centres and label to populate result image
// Mat &result_image = Mat(image.size(), image.type());
// for (int row = 0; row < image.rows; row++)
//   for (int col = 0; col < image.cols; col++)
//     for (int channel = 0; channel < 3; channel++)
//       result_image.at<Vec3b>(row, col)[channel] =
//           (uchar)centres.at<float>(*(labels.ptr<int>(
//                                        row * image.cols + col)),
//                                    channel);