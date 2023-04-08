const express = require('express');
const passport = require('passport');
const session = require('express-session');
const MongoStore = require('connect-mongo')(session);

const app = express();

// Passport Config
require('./config/passport')(passport);

// Connect to MongoDB
const mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/test', {
  useNewUrlParser: true,
  useCreateIndex: true,
  useUnifiedTopology: true,
  useFindAndModify: false
})
  .then(() => console.log('MongoDB Connected'))
  .catch((err) => console.log(err));

// Express body parser
app.use(express.urlencoded({ extended: true }));

// Express session
app.use(session({
  secret: 'secret',
  resave: false,
  saveUninitialized: false,
  store: new MongoStore({ mongooseConnection: mongoose.connection })
}));

// Passport middleware
app.use(passport.initialize());
app.use(passport.session());

// Routes
app.use('/', require('./routes/index'));
app.use('/users', require('./routes/users'));

const PORT = process.env.PORT || 5000;

app.listen(PORT, console.log(`Server started on port ${PORT}`));

##JOB_COMPLETE##