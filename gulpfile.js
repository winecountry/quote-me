const browserify = require('browserify'),
    browserSync = require('browser-sync').create(),
    source = require('vinyl-source-stream'),
    buffer = require('vinyl-buffer'),
    gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    babel = require('gulp-babel'),
    concat = require('gulp-concat'),
    gulpif = require('gulp-if'),
    sass = require("gulp-sass"),
    sassImage = require('gulp-sass-image'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify'),
    bourbon = require("node-bourbon").includePaths,
    normalize = require('node-normalize-scss').includePaths,
    path = require('path');
//a8c2 9bbf 0bcd
// environment
const DEVELOPMENT = 'development';
const PRODUCTION = 'production';
const env = process.env.NODE_ENV || DEVELOPMENT;
const BROWSERSYNC_PROXY = process.env.BROWSERSYNC_PROXY || "localhost:8000";

// define directories
const paths = {
    STATIC_ROOT: 'static',
    src: path.join('static', 'src'),
    sass: path.join('static', 'src', 'sass'),
    scripts: path.join('static', 'src', 'scripts'),
    dest: path.join('static', 'dist'),
    css: path.join('static', 'dist', 'css'),
    js: path.join('static', 'dist', 'js'),
    images: path.join('static', 'images'),
    templates: 'templates'
};

const masterSassSources = [ // master sass files
    path.join(paths.sass, 'style.scss')
], sassSources = [ // all sass files
    path.join(paths.sass, '/**/*.scss')
], jsSources = [ // all js scripts
    path.join(paths.scripts, '/**/*.js')
], templateSources = [
    path.join(paths.templates, '/**/*.html')
], imageSources = [
    path.join(paths.images, '/**/*.svg')
];

// interpret image urls from sass
gulp.task('sass-image', function () {
    return gulp.src(imageSources)
        .pipe(sassImage({
            images_path: 'static/images/',
            css_path: 'static/dist/css/'
        }))
        .pipe(gulp.dest(paths.sass))
});

// compile sass
gulp.task('sass', ['sass-image'], function () {
    gulp.src(masterSassSources)
        .pipe(gulpif(env === PRODUCTION, sourcemaps.init()))
        .pipe(sass({
            includePaths: [bourbon, normalize],
            outputStyle: env === PRODUCTION ? 'compressed' : 'expanded',
            errLogToConsole: true
        })).on('error', sass.logError)
        .pipe(gulpif(env === PRODUCTION, sourcemaps.write()))
        .pipe(autoprefixer())
        .pipe(gulp.dest(paths.css))
        .pipe(browserSync.stream());
});

// concatenate all js sources
gulp.task('js', function () {
    browserify({
            entries: path.join(paths.scripts, 'daily_quote.js'),
            debug: process.env === DEVELOPMENT
        })
        .bundle()
        .pipe(source('bundle.js'))
        .pipe(buffer())
        .pipe(gulpif(env === PRODUCTION, sourcemaps.init()))
        .pipe(babel({
            presets: ['env']
        }))
        .pipe(gulpif(env === PRODUCTION, uglify()))
        .pipe(gulpif(env === PRODUCTION, sourcemaps.write()))
        .pipe(gulp.dest(paths.js))
});

gulp.task('watch', function () {
    // reload page after html changes
    gulp.watch(templateSources).on('change', browserSync.reload);

    // update paths after image changes
    gulp.watch(imageSources, ['sass']);

    // inject css after sass changes
    gulp.watch(sassSources, ['sass']);

    // reload after js changes
    gulp.watch(jsSources, ['js']).on('change', browserSync.reload);
});

gulp.task('default', ['watch', 'sass', 'js'], function () {
    browserSync.init({
        proxy: BROWSERSYNC_PROXY
    });
});
