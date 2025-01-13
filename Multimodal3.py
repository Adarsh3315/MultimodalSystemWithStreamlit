import streamlit as st
import yfinance as yf


def fetch_and_display_stock_price(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        quote = stock.history(period="1d")
        if not quote.empty:
            price = quote["Close"].iloc[-1]
            if ".BO" in stock_symbol or ".NS" in stock_symbol:
                return f"₹{price:.2f} (INR)"
            else:
                return f"${price:.2f} (USD)"
        else:
            return "Invalid Stock Symbol Or Data Not Available."
    except ValueError as ve:
        return str(ve)
    except Exception as e:
        return f"An error occurred {str(e)}"


def stock_price_checker():
    st.markdown(
        """
        <p style="font-size: 18px; color: #004d40;">
        Enter Stock Symbol (Example: AMZN, TATASTEEL.BO, or TCS.NS) & Click 'Show Price' To Get The Current Stock Price.
        </p>
    """,
        unsafe_allow_html=True,
    )

    stock_symbol = st.text_input("Enter Stock Symbol:", value="", max_chars=50)

    if st.button("Show Price"):
        if stock_symbol.strip():
            stock_price = fetch_and_display_stock_price(stock_symbol.upper())
            st.success(f"Stock Price For {stock_symbol.upper()}: {stock_price}")
        else:
            st.error("Stock Symbol Cannot Be Empty.")


def main():
    st.title("Stock Market Price Checker")

    menu = ["Stock Market Price Checker"]
    choice = st.sidebar.selectbox("Select Model", menu)

    if choice == "Stock Market Price Checker":
        stock_price_checker()


if __name__ == "__main__":
    main()
