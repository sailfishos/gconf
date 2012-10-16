
# Force usage of gconf as gesttings backend as long as dconf is not available
# Otherwise memory backend is used and settings changes are not persistent

export GSETTINGS_BACKEND=gconf
