import logging
import os
import time
from io import BytesIO

import chromedriver_autoinstaller
import folium
from PIL import Image
from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from apps.mystories.models import Notification
from apps.users.models import ActiveSessions

logger = logging.getLogger(__name__)


@shared_task
def create_map_screenshot_and_notify(session_id):
    try:
        time.sleep(2)
        session = ActiveSessions.objects.get(id=session_id)
        location = session.location

        latitude = location.get("lat")
        longitude = location.get("lon")

        if latitude and longitude:
            map_object = folium.Map(
                location=[latitude, longitude], zoom_start=15, control_scale=True
            )
            folium.Marker([latitude, longitude], popup="Joylashuv").add_to(map_object)

            map_html = os.path.join(
                settings.BASE_DIR, f"assets/media/map_{session_id}.html"
            )
            screenshot_path = os.path.join(
                settings.BASE_DIR, f"assets/media/map_{session_id}.png"
            )

            media_dir = os.path.dirname(map_html)
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)

            map_object.save(map_html)
            logger.info(f"Map HTML saved to {map_html}")

            try:
                logger.info(f"Converting HTML to PNG: {map_html}")

                chromedriver_autoinstaller.install()

                options = webdriver.ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--hide-scrollbars")

                service = Service()
                driver = webdriver.Chrome(service=service, options=options)

                try:
                    driver.get(f"file://{os.path.abspath(map_html)}")
                    time.sleep(5)
                    driver.set_window_size(1920, 1080)
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved to {screenshot_path}")
                finally:
                    driver.quit()

                logger.info(f"Screenshot saved to {screenshot_path}")

                if not os.path.exists(screenshot_path):
                    logger.error(f"Screenshot not created: {screenshot_path}")
                    raise FileNotFoundError(f"File does not exist: {screenshot_path}")
                logger.info(f"Screenshot created: {screenshot_path}")

                with open(screenshot_path, "rb") as f:
                    image = Image.open(f)
                    webp_image_io = BytesIO()
                    image.save(webp_image_io, format="WEBP")
                    webp_image_io.seek(0)

                    filename = os.path.basename(screenshot_path)
                    sanitized_filename = (
                        f"{session.user.username}_session_{filename.split('.')[0]}.webp"
                    )

                notification = Notification.objects.create(
                    user=session.user,
                    title_uz="New session screenshot",
                    message_uz="A screenshot of your new session location has been created.",
                )
                logger.info(f"Notification created: {notification}")
                notification.banner.save(
                    sanitized_filename,
                    ContentFile(webp_image_io.read()),
                    save=False,
                )
                notification.save()
                logger.info(f"Notification banner saved: {notification.banner.url}")

                if os.path.exists(map_html):
                    os.remove(map_html)
                    logger.info(f"Deleted temporary HTML map file: {map_html}")
                if os.path.exists(screenshot_path):
                    os.remove(screenshot_path)
                    logger.info(f"Deleted temporary screenshot file: {screenshot_path}")
            except Exception as e:
                logger.error(f"Error generating image from HTML map: {e}")
                Notification.objects.create(
                    user=session.user,
                    title="New session",
                    message="A new session has been created, but the screenshot could not be generated.",
                )
        else:
            Notification.objects.create(user=session.user, title_uz="1", message_uz="1")

    except ActiveSessions.DoesNotExist:
        logger.error(f"ActiveSession with id {session_id} does not exist.")
    except Exception as e:
        logger.error(f"Error: {e}")
