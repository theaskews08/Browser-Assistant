from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from threading import Thread
import VINI_voice
from predict_intent import PredictIntent
import click_command_interpret
from click_command_interpret import get_the_objective
import tab_command_parser as tcp
from playsound import  Playsound

class Browser:
    up_interrupted=False
    down_interrupted=False
    links=[]
    inputs=[]
    selected_inpt=None
    
    def __init__(self,browser_name='firefox'):
        if browser_name=='firefox':
            self.browser=webdriver.Firefox()
        elif browser_name=='chrome':
            self.browser=webdriver.Chrome()
        self.ip = PredictIntent()
        self.original_style = None
  
    def back(self, command):  # simulates the click on the back button of the browser
        try:
            self.browser.back()
        except:
            print("The process  has disconnected from browser.")

    def forward(self, command):  # simulates the click on forward button
        try:
            self.browser.forward()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def quit(self, command):  # clicks the close window
        try:
            self.browser.quit()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def reload(self, command):  # clicks refresh button
        try:
            self.browser.refresh()
        except:
            print("Either The process  has disconnected from browser, or no forwarding possible")

    def scroll_down(self, command):  # scrolls down until interrupted
        self.up_interrupted=True
        self.down_interrupted=False
        def new_thread():
            try:
                while not self.down_interrupted:
                   self.browser.execute_script("window.scrollBy(0, 20);")
                   sleep(0.15)
                self.down_interrupted=False
                self.up_interrupted=False
            except:
                print("End of page reached")
        Thread(target=new_thread).start()

    def scroll_up(self, command):  # scrolls up until interrupted
        self.down_interrupted=True
        self.up_interrupted=False
        def new_thread2():
            try:
                while not self.up_interrupted:
                   self.browser.execute_script("window.scrollBy(0, -20);")
                   sleep(0.15)
                self.up_interrupted=False
                self.down_interrupted=False
            except:
                print("Beginning of page reached.")
        Thread(target=new_thread2).start()

    def stop_scrolling(self, command):  # stop
        self.up_interrupted=True
        self.down_interrupted=True

    def getPage(self,url):  # open a page
        self.url=url
        self.browser.get(url)
        self.getLinks()

    def getLinks(self): # get all  the links in a page
        self.links=self.browser.find_elements(By.TAG_NAME, 'a')
        self.links.extend(self.browser.find_elements(By.TAG_NAME, 'button'))
        
    def clickOn(self,element):  # clicks on an element
        element.click()

    def search(self,string):  # search google for something
        string = get_the_objective(string)
        # Use modern Google search URL format
        from urllib.parse import quote_plus
        search_query = quote_plus(string)
        self.getPage(f"https://www.google.com/search?q={search_query}")

    def highlight(self, element, toNormal = False):
        def apply_style(s):
            self.browser.execute_script("arguments[0].setAttribute('style', arguments[1]);",self.selected_inpt, s)
        if toNormal:
            apply_style(self.original_style)
            return 
        self.original_style = element.get_attribute('style')
        apply_style(self.original_style+";background: yellow;")
        
     	
    def findLink(self,string):
        print("got here")
        string = get_the_objective(string)
        string = string.lower().strip()

        # Check if the objective is a URL
        url_indicators = ['.com', '.org', '.net', '.edu', '.gov', '.io', '.co', '.uk', '.ca']
        is_url = any(indicator in string for indicator in url_indicators)

        if is_url:
            # If it looks like a URL, navigate directly to it
            if not string.startswith('http://') and not string.startswith('https://'):
                string = 'https://' + string
            print(f"Navigating to URL: {string}")
            self.getPage(string)
            return

        # Otherwise, search for and click a link on the page
        self.getLinks()

        # Filter out non-interactable elements
        interactable_links = []
        for link in self.links:
            try:
                # Skip elements that are not displayed or not enabled
                if not link.is_displayed() or not link.is_enabled():
                    continue
                # Skip hidden elements (like skip-to-content links)
                if 'skip' in link.get_attribute('class') or '':
                    if 'skip' in (link.get_attribute('class') or '').lower():
                        continue
                # Skip elements with no text and no aria-label
                text = link.text.strip()
                aria_label = link.get_attribute('aria-label') or ''
                if not text and not aria_label:
                    continue
                interactable_links.append(link)
            except:
                # If we can't check the element, skip it
                continue

        if not interactable_links:
            print("No interactable links found")
            return

        print(f"Found {len(interactable_links)} interactable links")
        queries = string.split()
        scores = [0] * len(interactable_links)

        for i in range(len(interactable_links)):
            try:
                text = interactable_links[i].text.lower()
                aria_label = (interactable_links[i].get_attribute('aria-label') or '').lower()
                combined_text = text + ' ' + aria_label

                for word in queries:
                    if word in combined_text:
                        scores[i] += 1
                if scores[i] == len(queries):  # early stopping to save time
                    break
            except:
                scores[i] = -1  # Mark as unusable
                continue

        # Find best candidates
        max_score = max(scores)
        if max_score <= 0:
            print("No matching links found")
            return

        print("found")

        # Try top 3 candidates
        for attempt in range(min(3, len(scores))):
            best_candidate_index = scores.index(max(scores))
            scores[best_candidate_index] = -1  # Mark as tried

            try:
                element = interactable_links[best_candidate_index]
                # Scroll element into view using JavaScript
                self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                sleep(0.3)
                # Try regular click first
                element.click()
                print(f"Successfully clicked element")
                return
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                # Try JavaScript click as fallback
                try:
                    self.browser.execute_script("arguments[0].click();", element)
                    print(f"Successfully clicked element using JavaScript")
                    return
                except Exception as e2:
                    print(f"JavaScript click also failed: {e2}")
                    continue

        print("Could not click any matching element")
        """
        try:
            self.clickOn(self.browser.find_element_by_link_text(string))
        except:
            try:
                self.clickOn(self.browser.find_element_by_link_text(string.capitalize()))
            except:    
                for _ in self.links:
                    if _.text.lower().startswith(string):
                        self.clickOn(_)
                        break"""

    def getInputs(self):
        self.inputs=self.browser.find_elements(By.TAG_NAME, 'input')
        self.inputs.extend(self.browser.find_elements(By.TAG_NAME, 'textarea'))

    def input_time(self):
        self.getInputs()
        self.selected_inpt = self.inputs[0]
        self.highlight(self.selected_inpt, toNormal = False)

    def enter_text(self, string):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range']
        try:
            if self.selected_inpt is None:
                self.input_time()
                self.enter_text("")
                return
            if not self.selected_inpt.is_displayed():
                self.next_input("")
                self.enter_text("")
                return
            if not self.selected_inpt.is_displayed():
                self.next_input("")
                self.enter_text("")
                return
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.next_input("")
                self.enter_text("")
                return
        except:
            self.input_time()
            self.enter_text("")
            return
        print("I am listening. Dictate the text in one go.")
        """beep sound here"""
        Playsound(True).start() #Blip sound
        b=VINI_voice.listen_for(7)
        
        #b = input("enter the text")
        intent = self.ip.predict_intent(b)
        if intent[0] == "next_input":
            Playsound().start() #Beep sound
            self.next_input("")
        elif intent[0] == "submit":
            Playsound().start() #Beep sound
            self.submit("")
        elif intent[0] == "previous_input":
            Playsound().start() #Beep sound
            self.previous_input("")
        if intent[0] == "clear":
            Playsound().start() #Beep sound
            self.clear_text("")
        else:
            try:
                self.selected_inpt.send_keys(b)
            except:
                return

    def clear_text(self, command):
        try:
            self.selected_inpt.clear()
        except:
            try:
                if self.selected_inpt is None:
                    self.input_time()
                    self.clear_text("")
                    return
                if not self.selected_inpt.is_displayed():
                    self.next_input("")
                    self.clear_text("")
                    return
                if not self.selected_inpt.is_displayed():
                    self.next_input("")
                    self.clear_text("")
                    return
                if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                    self.next_input("")
                    self.enter_text("")
                    return
            except:
                self.input_time()
                self.clear_text("")
                return
    
    def next_input(self, command):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range',""]
        try:
            self.getInputs()
            try:
                self.highlight(self.selected_inpt, toNormal = True) #unhighlight the previous input
            except:
                print("")
            self.selected_inpt = self.inputs[self.inputs.index(self.selected_inpt)+1]
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.next_input("")
                return
            self.highlight(self.selected_inpt, toNormal = False)
        except:
            return
        
    def previous_input(self, command):
        non_writable_inputs = ['radio', 'checkbox', 'button', 'color',
                               'file', 'hidden', 'image', 'month', 'range',""]
        if True:
            self.getInputs()
            try:
                self.highlight(self.selected_inpt, toNormal = True) #unhighlight the previous input
            except:
                print("")
            self.selected_inpt = self.inputs[self.inputs.index(self.selected_inpt)-1]
            if self.selected_inpt.get_attribute('type') in non_writable_inputs:
                self.previous_input("")
                return
            self.highlight(self.selected_inpt, toNormal = False)
        else:
            return
        
    def submit(self, command):
        try:
            self.selected_inpt.submit()
        except:
            return

    def open_new_tab(self, command):
        indx = len(self.browser.window_handles)
        try:
            self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL+ 't')
        except:
            self.browser.execute_script('''window.open("about:blank", "_blank");''')
        curWindowHndl = self.browser.current_window_handle
        self.browser.switch_to.window(self.browser.window_handles[indx])

    def close_tab(self, command):
        curWindowHndl = self.browser.current_window_handle
        print(curWindowHndl)
        self.browser.close()
        #after closing the current tab, switch to bext tab if available
        #otherwise the previous tab
        if len(self.browser.window_handles) >=1:
            #switch to the next greatest index
            indx = len(self.browser.window_handles) - 1
        self.browser.switch_to.window(self.browser.window_handles[indx])
        

    def switch_tab(self, command):
        #next/previous or n'th tab
        object = tcp.get_the_objective(command) #nothing to do with the TCP protocol though :P
        curWindowHndl = self.browser.current_window_handle
        current_indx = self.browser.window_handles.index(curWindowHndl)
        response = tcp.process_objective(object)
        if type(response) is str:
            if response == "+1":
                try:
                    self.browser.switch_to.window(self.browser.window_handles[current_indx + 1])
                except:
                    pass
            else:
                try:
                    self.browser.switch_to.window(self.browser.window_handles[current_indx - 1])
                except:
                    pass
        elif type(response) is int:
            if response < len(self.browser.window_handles):
                self.browser.switch_to.window(self.browser.window_handles[response])
            else:
                self.browser.switch_to.window(self.browser.window_handles[len(self.browser.window_handles) - 1])

