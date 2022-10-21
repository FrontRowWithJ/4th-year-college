// vector<vector<Point>> contours;
// vector<Vec4i> hierarchy;
// findContours(binary_edge_image, contours, hierarchy,
//              CV_RETR_CCOMP, CV_CHAIN_APPROX_NONE);
// for (int contour_number = 0;
//      (contour_number < contours.size()); contour_number++)
// {
//   Scalar colour(rand() & 0xFF, rand() & 0xFF, rand() & 0xFF);
//   drawContours(display_image, contours, contour_number,
//                colour, 1, 8, hierarchy);
// }