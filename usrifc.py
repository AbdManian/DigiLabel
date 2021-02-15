import tkinter as tk
import tkinter.filedialog as filedialog
import pagesizes
import labelmerger


class DigiLabelApplication(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(fill='both', expand=True)
        self.label_file_list = []
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        button_load_label_files = tk.Button(
            self, text="Add Labels", command=self.cmd_load_files)
        button_load_label_files.grid(row=0, column=0)
        button_clear_label_files = tk.Button(
            self, text="Clear Files", command=self.cmd_clear_files)
        button_clear_label_files.grid(row=0, column=2)
        button_generate_file = tk.Button(
            self, text="Generate", command=self.cmd_generate_files)
        button_generate_file.grid(row=0, column=1, sticky=tk.EW)
        self.listbox_file_list = tk.Listbox(self)
        self.listbox_file_list.grid(
            row=1, column=0, columnspan=3, sticky=tk.NSEW)

        sizes_frame = tk.Frame(self)
        sizes_frame.grid(row=2, column=0, columnspan=3, sticky=tk.NSEW)
        sizes_frame.columnconfigure(1, weight=1)
        self.size_dict = self.add_size_widgets_and_build_size_dict(sizes_frame)

    def cmd_clear_files(self):
        self.label_file_list.clear()
        self.listbox_file_list.delete(0, tk.END)

    def cmd_load_files(self):
        label_files = tk.filedialog.askopenfilenames(
            title='Select PDF labels',
            filetypes=(
                ("PDF files", "*.pdf"),
                ("All Files", "*.*")
            ))
        self.label_file_list.extend(label_files)
        for f_name in label_files:
            self.listbox_file_list.insert(tk.END, f_name)

    def cmd_generate_files(self):
        if not self.label_file_list:
            return

        output_file = tk.filedialog.asksaveasfilename(
            title='Set output PDF file',
            filetypes=(
                ("PDF files", "*.pdf"),
                ("All Files", "*.*")
            )
        )

        if not output_file:
            return

        labelmerger.do_label_merge(
            output_file,
            self.label_file_list,
            self.create_print_size_structure()
        )

    @staticmethod
    def create_size_entry_widgets(target_frame, row, text):
        label_widget = tk.Label(target_frame, text=text)
        label_widget.grid(row=row, column=0, sticky=tk.W)
        dvar = tk.DoubleVar()
        entry_widget = tk.Entry(target_frame, textvariable=dvar)
        entry_widget.grid(row=row, column=1, sticky=tk.EW)

        return dvar

    def add_size_widgets_and_build_size_dict(self, target_frame):
        label_sizes = tk.Label(target_frame, text='Print Sizes (in mm)')
        label_sizes.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        size_entry_list = [
            ('Print Width', 'print_width', 210),
            ('Print Height', 'print_height', 297),
            ('Print Top Margin', 'print_margin_top', 0),
            ('Print Right Margin', 'print_margin_right', 0),
            ('Print Bottom Margin', 'print_margin_bottom', 0),
            ('Print Left Margin', 'print_margin_left', 0),
            ('Label Width', 'label_width', 107),
            ('Label Height', 'label_height', 36),
            ('Label Top Margin', 'label_margin_top', 2),
            ('Label Right Margin', 'label_margin_right', 1),
            ('Label Bottom Margin', 'label_margin_bottom', 0),
            ('Label Left Margin', 'label_margin_left', 3),
        ]
        var_dict = dict()
        for rindex, (text, name, default_value) in enumerate(size_entry_list):
            dvar = self.create_size_entry_widgets(
                target_frame, rindex + 1, text)
            dvar.set(default_value)
            var_dict[name] = dvar
        return var_dict

    def create_print_size_structure(self):
        label_margins = pagesizes.PrintMargins(
            self.size_dict['label_margin_top'].get(),
            self.size_dict['label_margin_right'].get(),
            self.size_dict['label_margin_bottom'].get(),
            self.size_dict['label_margin_left'].get(),
        )

        label_page = pagesizes.PageSize(
            self.size_dict['label_height'].get(),
            self.size_dict['label_width'].get(),
            label_margins
        )

        page_margins = pagesizes.PrintMargins(
            self.size_dict['print_margin_top'].get(),
            self.size_dict['print_margin_right'].get(),
            self.size_dict['print_margin_bottom'].get(),
            self.size_dict['print_margin_left'].get(),
        )

        print_page = pagesizes.PageSize(
            self.size_dict['print_height'].get(),
            self.size_dict['print_width'].get(),
            page_margins
        )

        return pagesizes.LabelPrintSize(print_page, label_page)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('DigiLabel Creator')
    main = DigiLabelApplication(root)
    root.mainloop()
