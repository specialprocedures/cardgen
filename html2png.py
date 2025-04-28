import argparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def setup_webdriver(browser_name):
    if browser_name == "firefox":
        options = Options()
        options.add_argument("-headless")
        return webdriver.Firefox(options=options)
    elif browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        return webdriver.Chrome(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        return webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")


def html2png(
    html_path: Path,
    output_path: Path,
    element_class: str = "trading-card",
    browser: str = None,
    driver=None,
):
    """Convert HTML file to PNG.

    Args:
        html_path: Path to the HTML file to convert
        output_path: Path where the PNG should be saved
        element_class: CSS class name of element to screenshot (default: trading-card)
        browser: Browser to use for rendering if no driver provided (default: firefox)
        driver: Existing webdriver session to use (optional)
    """
    should_close_driver = False
    if driver is None:
        driver = setup_webdriver(browser or "firefox")
        should_close_driver = True

    try:
        # Load HTML file
        driver.get(f"file://{html_path.absolute()}")

        # Set scale for better quality
        driver.execute_script('document.body.style.MozTransform = "scale(5)";')
        driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

        # Find and screenshot specific element if class is provided
        if element_class:
            element = driver.find_element("class name", element_class)
            element.screenshot(str(output_path))
        else:
            # Take screenshot of entire page if no element class specified
            driver.save_screenshot(str(output_path))

        print(f"Generated PNG: {output_path}")

    finally:
        # Only close the driver if we created it
        if should_close_driver:
            driver.quit()


def main():
    parser = argparse.ArgumentParser(description="Convert HTML file to PNG")
    parser.add_argument(
        "html_file",
        type=Path,
        help="Path to HTML file to convert",
    )
    parser.add_argument(
        "output_file",
        type=Path,
        help="Path where PNG should be saved",
    )
    parser.add_argument(
        "--browser",
        type=str,
        choices=["firefox", "chrome", "edge"],
        default="firefox",
        help="Browser to use for rendering (default: firefox)",
    )
    parser.add_argument(
        "--element-class",
        type=str,
        default="trading-card",
        help="CSS class name of element to screenshot (default: trading-card). If not specified, screenshots entire page",
    )

    args = parser.parse_args()

    if not args.html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {args.html_file}")

    # Create output directory if it doesn't exist
    args.output_file.parent.mkdir(parents=True, exist_ok=True)

    html2png(args.html_file, args.output_file, args.element_class, args.browser)


if __name__ == "__main__":
    main()
