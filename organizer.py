from bs4 import BeautifulSoup
import os

class PageManager:
    def __init__(self, index_file="index.html"):
        self.index_file = index_file
        with open(index_file, "r", encoding="utf-8") as f:
            self.soup = BeautifulSoup(f, "html.parser")
    def _update_links(self):
        toc_body = self.soup.find("body", id="table of content")
        all_links = [link["href"] for link in toc_body.find_all("a")]

        for index, link in enumerate(all_links):
            with open(link, "r", encoding="utf-8") as f:
                chapter_soup = BeautifulSoup(f, "html.parser")

            dir_div = chapter_soup.find("div", id="dir")
            [a.extract() for a in dir_div.find_all("a") if "Previous" in a.text or "Next" in a.text]

            if index > 0:
                prev_a = chapter_soup.new_tag("a", href=all_links[index - 1])
                prev_a.string = "Previous Chapter <<"
                dir_div.append(prev_a)
                #dir_div.append(chapter_soup.new_tag("br"))

            if index < len(all_links) - 1:
                next_a = chapter_soup.new_tag("a", href=all_links[index + 1])
                next_a.string = "Next Chapter >>"
                dir_div.append(next_a)
                #dir_div.append(chapter_soup.new_tag("br"))

            with open(link, "w", encoding="utf-8") as f:
                f.write(str(chapter_soup))

    def add_page(self, filename, page_name):
        new_li = self.soup.new_tag("li")
        new_a = self.soup.new_tag("a", href=filename)
        new_a.string = page_name
        new_li.append(new_a)
        self.soup.ul.append(new_li)
        self._update_links()

    def remove_page(self, filename):
        for a in self.soup.find_all("a", href=filename):
            a.parent.decompose()
        os.remove(filename)  # Remove the file
        self._update_links()

    def insert_page(self, filename, page_name, position):
        new_li = self.soup.new_tag("li")
        new_a = self.soup.new_tag("a", href=filename)
        new_a.string = page_name
        new_li.append(new_a)
        all_links = self.soup.ul.find_all("li")
        all_links[position].insert_before(new_li)
        self._update_links()

    def rename_page(self, old_filename, new_filename, new_name):
        for a in self.soup.find_all("a", href=old_filename):
            a["href"] = new_filename
            a.string = new_name
        os.rename(old_filename, new_filename) 
        self._update_links()

    def save(self):
        with open(self.index_file, "w", encoding="utf-8") as f:
            f.write(str(self.soup))

manager = PageManager()
#demo
# manager.add_page("3.html", "Chapter3")
# manager._update_links()
# manager.save()
