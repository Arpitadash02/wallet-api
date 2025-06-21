# makes 'routes' folder a package
from .auth_routes import bp as auth_routes
from .wallet_routes import bp as wallet_routes
from .product_routes import bp as product_routes