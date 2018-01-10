const gulp = require('gulp'),
    gutil = require('gulp-util'),
    browserify = require('gulp-browserify'),
    compass = require('gulp-compass'),
    concat = require('gulp-concat'),
    path = require('path');

const STATIC_ROOT = 'static';
const src = path.join(STATIC_ROOT, 'src');
const dest = path.join(STATIC_ROOT, 'dist');
const image = path.join(STATIC_ROOT, 'images');
const css = path.join(dest, 'css');
const js = path.join(dest, 'js');
const sass = path.join(src, 'sass');

const sassSources = [
    path.join(sass, 'style.scss')
];

gulp.task('compass', function () {
    gulp.src(sassSources)
        .pipe(compass({
            css: css,
            sass: sass,
            image: image,
            style: 'expanded'
        }))
        .pipe(gulp.dest(css))
});

const jsSources = [
    path.join(src, 'scripts', '*.js')
];

gulp.task('js', function () {
    gulp.src(jsSources)
        .pipe(concat('script.js'))
        .pipe(browserify())
        .pipe(gulp.dest(js))
});

gulp.task('default', ['js', 'compass']);
