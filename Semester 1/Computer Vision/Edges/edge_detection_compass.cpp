// Mat horizontal_derivative, vertical_derivative;
// Sobel(gray_image, horizontal_derivative, CV_32F, 1, 0);
// Sobel(gray_image, vertical_derivative, CV_32F, 0, 1);
// Mat abs_gradient, l2norm_gradient, orientation;
// abs_gradient = abs(horizontal_derivative) +
//                abs(vertical_derivative);
// cartToPolar(horizontal_derivative, vertical_derivative,
//             l2norm_gradient, orientation);